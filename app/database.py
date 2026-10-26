import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def connect(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path):
    with connect(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            action TEXT NOT NULL,
            schedule_type TEXT NOT NULL CHECK(schedule_type IN ('once','interval')),
            run_at TEXT,
            interval_minutes INTEGER,
            next_run TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            duration_seconds REAL,
            exit_code INTEGER,
            stdout TEXT,
            stderr TEXT,
            FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            event TEXT NOT NULL,
            created_at TEXT NOT NULL,
            details TEXT,
            FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE SET NULL
        );
        """)

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def log_event(conn, event, task_id=None, details=""):
    conn.execute(
        "INSERT INTO events(task_id,event,created_at,details) VALUES(?,?,?,?)",
        (task_id, event, utc_now(), details)
    )
