"""Strictly scoped memory retrieval for project brains and the master orchestrator."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime
from core.storage import connect, now, rows

MASTER = "master"
ROOT = Path(__file__).resolve().parents[1]

def project_scope(project: str) -> str:
    if not project or ":" in project or "/" in project or ".." in project:
        raise ValueError("Invalid project scope")
    return f"project:{project}"

def remember(scope_id: str, content: str, kind: str = "note", source_id: str | None = None) -> int:
    if scope_id != MASTER and not scope_id.startswith(("project:", "job:", "agent:")):
        raise ValueError("Invalid scope")
    with connect() as db:
        cur=db.execute("INSERT INTO memories(scope_id,kind,content,source_id,created_at) VALUES(?,?,?,?,?)",(scope_id,kind,content,source_id,now()))
        return int(cur.lastrowid)

def recall(scope_id: str, query: str = "", limit: int = 25):
    sql="SELECT * FROM memories WHERE scope_id=?"; params=[scope_id]
    if query.strip(): sql+=" AND content LIKE ?"; params.append(f"%{query.strip()}%")
    sql+=" ORDER BY id DESC LIMIT ?"; params.append(limit)
    return rows(sql,tuple(params))

def scope_summary(project: str) -> dict:
    scope=project_scope(project)
    return {"scope_id":scope,"memories":len(recall(scope,limit=10000)),"documents":rows("SELECT count(*) n FROM documents WHERE scope_id=?",(scope,))[0]["n"],"jobs":rows("SELECT count(*) n FROM jobs WHERE scope_id=?",(scope,))[0]["n"]}


def get_project_path(project_name: str) -> Path:
    """Get the project directory."""
    return ROOT / "ideas" / project_name


def get_active_session(project_name: str) -> str:
    """Read agent's active session state — temporary scratch for current task."""
    session_file = get_project_path(project_name) / ".active_session.md"
    if session_file.exists():
        return session_file.read_text()
    return ""


def set_active_session(project_name: str, content: str):
    """Write agent's active session state."""
    session_file = get_project_path(project_name) / ".active_session.md"
    session_file.write_text(content)


def get_project_brain(project_name: str) -> dict:
    """Read project brain (permanent memory that never gets wiped)."""
    project_dir = get_project_path(project_name)
    brain = {}
    for name in ["README.md", "GOALS.md", "PROMPT.md", "MEMORY.md"]:
        path = project_dir / name
        brain[name] = path.read_text() if path.exists() else ""
    return brain


def reset_agent(project_name: str) -> dict:
    """
    Clear only the active session, archive it to master memory.
    Project brain (MEMORY.md, GOALS.md, PROMPT.md) is never touched.
    """
    session_file = get_project_path(project_name) / ".active_session.md"
    content = session_file.read_text() if session_file.exists() else ""

    if content.strip():
        # Archive to memory_archive table via master scope
        archive_scope = project_scope(project_name)
        remember(archive_scope, f"[{datetime.now().isoformat()}]\n{content}", kind="archived_session")

    # Only clear the session file, never touch project brain
    session_file.write_text("")
    return {"ok": True, "archived_bytes": len(content.encode())}


def get_project_history(project_name: str, limit: int = 20):
    """Read archived sessions for this project."""
    archive_scope = project_scope(project_name)
    results = recall(archive_scope, limit=limit)
    return [r for r in results if r["kind"] == "archived_session"]
