import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = "database/wizard_os.db"


def init_db() -> None:
    """Initializes the SQLite database and creates the workflow_runs table if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_runs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            task_description TEXT NOT NULL,
            status TEXT NOT NULL,
            total_tasks INTEGER,
            avg_success_rate REAL,
            top_agent TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[Database] SQLite initialized and tables verified successfully.")


def save_task_run(
    task_description: str,
    status: str,
    total_tasks: int,
    avg_success_rate: float,
    top_agent: str
) -> None:
    """Persists a completed multi-agent workflow execution to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO workflow_runs (timestamp, task_description, status, total_tasks, avg_success_rate, top_agent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, task_description, status, total_tasks, avg_success_rate, top_agent))
    conn.commit()
    conn.close()
    print("[Database] Workflow metrics successfully persisted to SQLite.")


def fetch_recent_runs(limit: int = 5) -> List[Tuple]:
    """Retrieves the most recent workflow executions from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, task_description, status, total_tasks, avg_success_rate, top_agent
        FROM workflow_runs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows