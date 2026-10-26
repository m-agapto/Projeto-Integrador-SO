import csv
import io
from datetime import datetime, timedelta, timezone
from flask import Blueprint, current_app, flash, redirect, render_template, request, Response, url_for
from .database import connect, utc_now, log_event
from .task_runner import ALLOWED_ACTIONS

bp = Blueprint("main", __name__)

def _iso_from_local(value):
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        # Browser local time is accepted as UTC in this starter project.
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()

@bp.get("/")
def index():
    with connect(current_app.config["DATABASE"]) as conn:
        tasks = conn.execute("""
            SELECT t.*,
              (SELECT status FROM runs WHERE task_id=t.id ORDER BY id DESC LIMIT 1) AS last_status,
              (SELECT started_at FROM runs WHERE task_id=t.id ORDER BY id DESC LIMIT 1) AS last_run
            FROM tasks t ORDER BY t.id DESC
        """).fetchall()
        recent_runs = conn.execute("""
            SELECT r.*, t.name AS task_name FROM runs r
            JOIN tasks t ON t.id=r.task_id ORDER BY r.id DESC LIMIT 8
        """).fetchall()
        stats = {
            "total": conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            "enabled": conn.execute("SELECT COUNT(*) FROM tasks WHERE enabled=1").fetchone()[0],
            "success": conn.execute("SELECT COUNT(*) FROM runs WHERE status='concluída'").fetchone()[0],
            "failed": conn.execute("SELECT COUNT(*) FROM runs WHERE status='falhou'").fetchone()[0],
        }
    return render_template("index.html", tasks=tasks, recent_runs=recent_runs,
                           stats=stats, actions=ALLOWED_ACTIONS, now=datetime.now(timezone.utc))

@bp.post("/tasks")
def create_task():
    name = request.form.get("name", "").strip()
    action = request.form.get("action", "")
    schedule_type = request.form.get("schedule_type", "")
    if not name or len(name) > 80:
        flash("Informe um nome com até 80 caracteres.", "error")
        return redirect(url_for("main.index"))
    if action not in ALLOWED_ACTIONS:
        flash("Ação inválida ou não autorizada.", "error")
        return redirect(url_for("main.index"))
    if schedule_type not in ("once", "interval"):
        flash("Tipo de agendamento inválido.", "error")
        return redirect(url_for("main.index"))

    try:
        if schedule_type == "once":
            run_at = _iso_from_local(request.form.get("run_at", ""))
            if datetime.fromisoformat(run_at) <= datetime.now(timezone.utc):
                raise ValueError("O horário deve estar no futuro.")
            next_run = run_at
            interval = None
        else:
            interval = int(request.form.get("interval_minutes", ""))
            if not 1 <= interval <= 10080:
                raise ValueError("O intervalo deve estar entre 1 e 10080 minutos.")
            run_at = None
            next_run = (datetime.now(timezone.utc) + timedelta(minutes=interval)).replace(microsecond=0).isoformat()
    except (ValueError, TypeError):
        flash("Confira o horário ou intervalo informado. O horário único deve estar no futuro e o intervalo entre 1 e 10080 minutos.", "error")
        return redirect(url_for("main.index"))

    with connect(current_app.config["DATABASE"]) as conn:
        cur = conn.execute("""
            INSERT INTO tasks(name, action, schedule_type, run_at, interval_minutes,
                              next_run, enabled, created_at)
            VALUES(?,?,?,?,?,?,1,?)
        """, (name, action, schedule_type, run_at, interval, next_run, utc_now()))
        log_event(conn, "tarefa criada", cur.lastrowid, name)
    flash("Tarefa cadastrada com sucesso.", "success")
    return redirect(url_for("main.index"))

@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with connect(current_app.config["DATABASE"]) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not task:
            flash("Tarefa não encontrada.", "error")
        elif task["schedule_type"] == "once" and not task["enabled"]:
            flash("Esta tarefa única já foi executada ou desativada.", "error")
        else:
            enabled = 0 if task["enabled"] else 1
            conn.execute("UPDATE tasks SET enabled=? WHERE id=?", (enabled, task_id))
            log_event(conn, "tarefa pausada" if not enabled else "tarefa reativada", task_id)
            flash("Tarefa atualizada.", "success")
    return redirect(url_for("main.index"))

@bp.post("/tasks/<int:task_id>/cancel")
def cancel_task(task_id):
    with connect(current_app.config["DATABASE"]) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not task:
            flash("Tarefa não encontrada.", "error")
        else:
            conn.execute("UPDATE tasks SET enabled=0 WHERE id=?", (task_id,))
            log_event(conn, "tarefa cancelada", task_id)
            flash("Tarefa cancelada/desativada.", "success")
    return redirect(url_for("main.index"))

@bp.get("/tasks/<int:task_id>")
def task_detail(task_id):
    with connect(current_app.config["DATABASE"]) as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not task:
            flash("Tarefa não encontrada.", "error")
            return redirect(url_for("main.index"))
        runs = conn.execute("SELECT * FROM runs WHERE task_id=? ORDER BY id DESC", (task_id,)).fetchall()
        events = conn.execute("SELECT * FROM events WHERE task_id=? ORDER BY id DESC LIMIT 30", (task_id,)).fetchall()
    return render_template("task_detail.html", task=task, runs=runs, events=events, actions=ALLOWED_ACTIONS)

@bp.get("/runs.csv")
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "tarefa", "status", "inicio", "fim", "duracao_segundos", "codigo_saida"])
    with connect(current_app.config["DATABASE"]) as conn:
        rows = conn.execute("""
            SELECT r.id, t.name, r.status, r.started_at, r.finished_at,
                   r.duration_seconds, r.exit_code
            FROM runs r JOIN tasks t ON t.id=r.task_id ORDER BY r.id DESC
        """).fetchall()
        writer.writerows([tuple(row) for row in rows])
    return Response("\ufeff" + output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=historico_execucoes.csv"})
