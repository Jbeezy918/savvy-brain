"""Recoverable project approval and release promotion."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from core.storage import ROOT, connect, log, now


def request_approval(project: str, source_path: str, note: str = "") -> int:
    source = Path(source_path).resolve()
    project_root = (ROOT / "ideas" / project).resolve()
    if project_root not in source.parents or source.parent.name != "outputs":
        raise ValueError("Only files in this project's outputs folder can be submitted")
    with connect() as db:
        cursor = db.execute(
            "INSERT INTO approvals(project,source_path,note,status,requested_at) VALUES(?,?,?,'pending',?)",
            (project, str(source), note, now()),
        )
        approval_id = int(cursor.lastrowid)
    log("approval_requested", f"Approval {approval_id}: {source.name}", project)
    return approval_id


def decide(approval_id: int, approve: bool) -> Path | None:
    with connect() as db:
        item = db.execute("SELECT * FROM approvals WHERE id=?", (approval_id,)).fetchone()
    if not item or item["status"] != "pending":
        raise ValueError("Approval is missing or already decided")
    if not approve:
        with connect() as db:
            db.execute("UPDATE approvals SET status='rejected',decided_at=? WHERE id=?", (now(), approval_id))
        log("approval_rejected", f"Approval {approval_id}", item["project"])
        return None
    project_root = (ROOT / "ideas" / item["project"]).resolve()
    source = Path(item["source_path"]).resolve()
    if project_root not in source.parents or source.parent.name != "outputs" or not source.is_file():
        raise ValueError("Approval source is no longer valid")
    version = datetime.now(timezone.utc).strftime("v%Y%m%d-%H%M%S")
    release = project_root / "releases" / version
    release.mkdir(parents=True, exist_ok=False)
    shutil.copy2(source, release / source.name)
    manifest = {"version": version, "approved_at": now(), "source": source.name, "note": item["note"]}
    (release / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (project_root / "releases" / "current.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with connect() as db:
        db.execute("UPDATE approvals SET status='approved',decided_at=?,release_path=? WHERE id=?",
                   (now(), str(release), approval_id))
    log("release_approved", str(release), item["project"])
    return release

