import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wizard_os.db")


def init_db():
    """Initializes the SQLite database and creates the required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing agent task execution history and analysis results
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS task_history
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       task_description
                       TEXT,
                       status
                       TEXT,
                       total_tasks
                       INTEGER,
                       avg_success_rate
                       REAL,
                       top_agent
                       TEXT,
                       timestamp
                       DATETIME
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   """)

    conn.commit()
    conn.close()
    print("[Database] SQLite initialized and tables verified successfully.")


def save_task_run(task_description: str, status: str, total_tasks: int, avg_success_rate: float, top_agent: str):
    """Saves a completed workflow run into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO task_history (task_description, status, total_tasks, avg_success_rate, top_agent)
                   VALUES (?, ?, ?, ?, ?)
                   """, (task_description, status, total_tasks, avg_success_rate, top_agent))

    conn.commit()
    conn.close()
    print("[Database] Workflow metrics successfully persisted to SQLite.")


if __name__ == "__main__":
    init_db()