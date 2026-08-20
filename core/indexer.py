"""Safe text-file indexer for the Savvy Brain workspace."""

from __future__ import annotations

from pathlib import Path

from core.storage import ROOT, connect, log, now

TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".csv", ".toml"}
IGNORED = {".git", ".venv", "__pycache__", "data"}
MAX_BYTES = 1_000_000


def project_for(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT / "ideas")
        return relative.parts[0]
    except ValueError:
        return None


def index_workspace() -> tuple[int, int]:
    indexed = skipped = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > MAX_BYTES:
            skipped += 1
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            skipped += 1
            continue
        relative = str(path.relative_to(ROOT))
        with connect() as db:
            db.execute(
                """INSERT INTO documents(path,project,modified,size,content,indexed_at)
                VALUES(?,?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET
                project=excluded.project,modified=excluded.modified,size=excluded.size,
                content=excluded.content,indexed_at=excluded.indexed_at""",
                (relative, project_for(path), path.stat().st_mtime, path.stat().st_size, content, now()),
            )
            project=project_for(path)
            db.execute("UPDATE documents SET scope_id=? WHERE path=?",(f"project:{project}" if project else "master",relative))
        indexed += 1
    log("index_complete", f"Indexed {indexed}; skipped {skipped}")
    return indexed, skipped


def search(query: str, limit: int = 30, scope_id: str | None = None):
    if not query.strip():
        return []
    with connect() as db:
        scope_sql=" AND d.scope_id=?" if scope_id else ""
        params=(query,scope_id,limit) if scope_id else (query,limit)
        return db.execute(
            """SELECT d.path,d.project,snippet(documents_fts,2,'[',']',' … ',16) snippet
            FROM documents_fts JOIN documents d ON d.rowid=documents_fts.rowid
            WHERE documents_fts MATCH ?"""+scope_sql+" ORDER BY rank LIMIT ?",
            params,
        ).fetchall()
