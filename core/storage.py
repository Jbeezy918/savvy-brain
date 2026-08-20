"""SQLite persistence for projects, indexed documents, jobs, and activity."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "savvy_brain.db"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=30)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize() -> None:
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
          path TEXT PRIMARY KEY, project TEXT, modified REAL, size INTEGER,
          content TEXT NOT NULL, indexed_at TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
          path, project, content, content='documents', content_rowid='rowid'
        );
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
          INSERT INTO documents_fts(rowid,path,project,content)
          VALUES (new.rowid,new.path,new.project,new.content);
        END;
        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
          INSERT INTO documents_fts(documents_fts,rowid,path,project,content)
          VALUES ('delete',old.rowid,old.path,old.project,old.content);
        END;
        CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
          INSERT INTO documents_fts(documents_fts,rowid,path,project,content)
          VALUES ('delete',old.rowid,old.path,old.project,old.content);
          INSERT INTO documents_fts(rowid,path,project,content)
          VALUES (new.rowid,new.path,new.project,new.content);
        END;
        CREATE TABLE IF NOT EXISTS jobs (
          id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT NOT NULL,
          prompt TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued',
          provider TEXT NOT NULL DEFAULT 'ollama', model TEXT,
          created_at TEXT NOT NULL, started_at TEXT, finished_at TEXT,
          output_path TEXT, error TEXT
        );
        CREATE TABLE IF NOT EXISTS activity (
          id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL,
          project TEXT, event TEXT NOT NULL, detail TEXT
        );
        CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
          role TEXT NOT NULL, content TEXT NOT NULL, project TEXT,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS milestones (
          id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT NOT NULL,
          title TEXT NOT NULL, detail TEXT, status TEXT NOT NULL DEFAULT 'planned',
          created_at TEXT NOT NULL, completed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS approvals (
          id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT NOT NULL,
          source_path TEXT NOT NULL, note TEXT, status TEXT NOT NULL DEFAULT 'pending',
          requested_at TEXT NOT NULL, decided_at TEXT, release_path TEXT
        );
        """)
        _migrate(db)


def _columns(db, table: str) -> set[str]:
    return {row[1] for row in db.execute(f"PRAGMA table_info({table})")}


def _migrate(db) -> None:
    """Idempotent migrations. Every retrievable record receives an explicit scope."""
    for table in ("documents", "jobs", "activity", "messages", "milestones", "approvals"):
        if "scope_id" not in _columns(db, table):
            db.execute(f"ALTER TABLE {table} ADD COLUMN scope_id TEXT")
        db.execute(f"UPDATE {table} SET scope_id=CASE WHEN project IS NULL OR project='' THEN 'master' ELSE 'project:'||project END WHERE scope_id IS NULL OR scope_id='' ")
    db.executescript("""
      CREATE INDEX IF NOT EXISTS idx_documents_scope ON documents(scope_id);
      CREATE INDEX IF NOT EXISTS idx_jobs_scope ON jobs(scope_id,status);
      CREATE INDEX IF NOT EXISTS idx_messages_scope ON messages(scope_id,created_at);
      CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT, scope_id TEXT NOT NULL,
        kind TEXT NOT NULL DEFAULT 'note', content TEXT NOT NULL,
        source_id TEXT, created_at TEXT NOT NULL,
        UNIQUE(scope_id,kind,source_id)
      );
      CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(scope_id,created_at);
      CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY,value TEXT NOT NULL,updated_at TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS ingestion_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT, source_path TEXT NOT NULL UNIQUE,
        source_type TEXT NOT NULL, sha256 TEXT, size INTEGER, modified REAL,
        scope_id TEXT NOT NULL, status TEXT NOT NULL, review_reason TEXT,
        staged_path TEXT, discovered_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_ingestion_scope ON ingestion_items(scope_id,status);
      CREATE TABLE IF NOT EXISTS knowledge_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT, scope_id TEXT NOT NULL,
        profile_type TEXT NOT NULL, statement TEXT NOT NULL, source_path TEXT NOT NULL,
        confidence REAL NOT NULL DEFAULT 0.6, created_at TEXT NOT NULL,
        UNIQUE(scope_id,profile_type,statement,source_path)
      );
      CREATE INDEX IF NOT EXISTS idx_profiles_scope ON knowledge_profiles(scope_id,profile_type);
      CREATE TABLE IF NOT EXISTS worker_restarts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT NOT NULL,
        restarted_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_worker_restarts_project ON worker_restarts(project,restarted_at);
    """)


def log(event: str, detail: str = "", project: str | None = None) -> None:
    with connect() as db:
        db.execute("INSERT INTO activity(created_at,project,event,detail) VALUES(?,?,?,?)",
                   (now(), project, event, detail))


def enqueue(project: str, prompt: str, provider: str, model: str) -> int:
    with connect() as db:
        cursor = db.execute(
            "INSERT INTO jobs(project,prompt,status,provider,model,created_at,scope_id) VALUES(?,?,'queued',?,?,?,?)",
            (project, prompt, provider, model, now(), f"project:{project}"),
        )
        job_id = int(cursor.lastrowid)
    log("job_queued", f"Job {job_id}", project)
    return job_id


def rows(query: str, parameters: tuple = ()) -> list[sqlite3.Row]:
    with connect() as db:
        return list(db.execute(query, parameters).fetchall())


def add_message(session_id: str, role: str, content: str, project: str | None = None) -> None:
    with connect() as db:
        db.execute("INSERT INTO messages(session_id,role,content,project,created_at,scope_id) VALUES(?,?,?,?,?,?)",
                   (session_id, role, content, project, now(), f"project:{project}" if project else "master"))


def get_setting(key: str, default: str = "") -> str:
    found = rows("SELECT value FROM settings WHERE key=?", (key,))
    return found[0]["value"] if found else default


def set_setting(key: str, value: str) -> None:
    with connect() as db:
        db.execute("INSERT INTO settings(key,value,updated_at) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at", (key, value, now()))
