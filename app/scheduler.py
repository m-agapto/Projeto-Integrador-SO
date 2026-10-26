import threading
import os
import time
from datetime import datetime, timezone
from .database import connect, utc_now, log_event
from .task_runner import execute_action

_started = set()
_lock = threading.Lock()

def _parse_time(value):
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def run_task(app, task):
    db_path = app.config["DATABASE"]
    log_dir = app.config["LOG_DIR"]
    start = utc_now()
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO runs(task_id,status,started_at) VALUES(?,?,?)",
            (task["id"], "em execução", start)
        )
        run_id = cur.lastrowid
        log_event(conn, "execução iniciada", task["id"], f"run_id={run_id}")

    try:
        result = execute_action(task["action"], log_dir)
    except Exception as exc:
        result = {
            "status": "falhou", "exit_code": -1,
            "stdout": "", "stderr": f"{type(exc).__name__}: {exc}",
            "duration": 0.0,
        }

    finished = utc_now()
    with connect(db_path) as conn:
        conn.execute("""
            UPDATE runs SET status=?, finished_at=?, duration_seconds=?,
                exit_code=?, stdout=?, stderr=? WHERE id=?
        """, (result["status"], finished, result["duration"], result["exit_code"],
              result["stdout"], result["stderr"], run_id))
        log_event(conn, f"execução {result['status']}", task["id"],
                  f"run_id={run_id}; exit_code={result['exit_code']}")

        if task["schedule_type"] == "once":
            conn.execute("UPDATE tasks SET enabled=0 WHERE id=?", (task["id"],))
        else:
            next_run = datetime.now(timezone.utc).timestamp() + int(task["interval_minutes"]) * 60
            next_iso = datetime.fromtimestamp(next_run, timezone.utc).replace(microsecond=0).isoformat()
            conn.execute("UPDATE tasks SET next_run=? WHERE id=?", (next_iso, task["id"]))

def _loop(app, stop_event):
    while not stop_event.is_set():
        now = datetime.now(timezone.utc)
        try:
            with app.app_context():
                with connect(app.config["DATABASE"]) as conn:
                    rows = conn.execute("""
                        SELECT * FROM tasks
                        WHERE enabled=1 AND next_run <= ?
                        ORDER BY next_run ASC
                    """, (now.replace(microsecond=0).isoformat(),)).fetchall()
                for task in rows:
                    with _lock:
                        if task["id"] in _started:
                            continue
                        _started.add(task["id"])
                    try:
                        run_task(app, dict(task))
                    finally:
                        with _lock:
                            _started.discard(task["id"])
        except Exception:
            app.logger.exception("Erro no ciclo do agendador")
        stop_event.wait(2)

def start_scheduler(app):
    # Avoid starting a second background scheduler in Flask's debug reloader child/parent.
    if app.testing or app.config.get("DISABLE_SCHEDULER"):
        return
    if app.debug and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return
    stop_event = threading.Event()
    thread = threading.Thread(target=_loop, args=(app, stop_event), daemon=True,
                              name="agendador-web")
    thread.start()
