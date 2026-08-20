"""Grounded central assistant for project and tool status."""

from __future__ import annotations

import json
from pathlib import Path

from core.brain import generate
from core.indexer import search
from core.storage import ROOT, rows


def system_snapshot(project: str | None = None) -> str:
    folders = [ROOT / "ideas" / project] if project else sorted((ROOT / "ideas").iterdir())
    report = []
    for folder in folders:
        if not folder.is_dir():
            continue
        completed = rows("SELECT count(*) n FROM jobs WHERE project=? AND status='completed'", (folder.name,))[0]["n"]
        waiting = rows("SELECT count(*) n FROM approvals WHERE project=? AND status='pending'", (folder.name,))[0]["n"]
        current = folder / "releases" / "current.json"
        release = json.loads(current.read_text(encoding="utf-8"))["version"] if current.exists() else "none approved"
        outputs = len(list((folder / "outputs").glob("*.md")))
        report.append(f"{folder.name}: completed jobs={completed}, outputs={outputs}, waiting approvals={waiting}, official release={release}")
    tools = ", ".join(sorted(p.name for p in (ROOT / "tools").glob("*.*"))) or "none"
    recent = rows("SELECT created_at,project,event,detail FROM activity ORDER BY id DESC LIMIT 12")
    activity = "\n".join(f"{r['created_at']} {r['project'] or 'system'} {r['event']}: {r['detail']}" for r in recent)
    return f"PROJECT STATUS\n" + "\n".join(report) + f"\n\nTOOLS\n{tools}\n\nRECENT ACTIVITY\n{activity}"


def answer(question: str, project: str | None, provider: str, model: str) -> str:
    snapshot = system_snapshot(project)
    try:
        hits = search(question, limit=8)
        evidence = "\n".join(f"{h['path']}: {h['snippet']}" for h in hits)
    except Exception:
        evidence = ""
    system = (
        "You are Savvy, Joe's local project command assistant. Address him as Joe naturally, but not in every sentence. "
        "Answer using only the supplied system snapshot and indexed evidence. State when information is missing. "
        "Never claim background work occurred unless it appears in activity. Clearly identify anything waiting for approval. "
        "Be concise and conversational because your answer may be spoken aloud.\n\n"
        f"{snapshot}\n\nINDEXED EVIDENCE\n{evidence}"
    )
    return generate(provider, model, system, question)

