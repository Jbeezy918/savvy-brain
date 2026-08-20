"""Bounded queue worker. It writes proposals only inside project outputs folders."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.brain import generate, load_project  # noqa: E402
from core.storage import connect, initialize, log, now  # noqa: E402


def claim(project: str | None = None):
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        if project:
            job = db.execute("SELECT * FROM jobs WHERE status='queued' AND project=? ORDER BY id LIMIT 1", (project,)).fetchone()
        else:
            job = db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY id LIMIT 1").fetchone()
        if job:
            db.execute("UPDATE jobs SET status='running',started_at=? WHERE id=?", (now(), job["id"]))
        return job


def run_one(project: str | None = None) -> bool:
    job = claim(project)
    if not job:
        return False
    try:
        folder, config, context = load_project(job["project"])
        guardrail = (
            "Return a concrete development proposal in Markdown. Do not claim to have changed files, "
            "contacted people, spent money, or executed external actions. Clearly list assumptions and next steps."
        )
        result = generate(job["provider"], job["model"] or config["model"], f"{guardrail}\n\n{context}", job["prompt"])
        output_dir = folder / "outputs"
        output_dir.mkdir(exist_ok=True)
        output = output_dir / f"job-{job['id']}.md"
        output.write_text(f"# Job {job['id']} Output\n\n{result}\n", encoding="utf-8")
        with connect() as db:
            db.execute("UPDATE jobs SET status='completed',finished_at=?,output_path=? WHERE id=?",
                       (now(), str(output), job["id"]))
        log("job_completed", str(output), job["project"])
    except Exception as exc:
        with connect() as db:
            db.execute("UPDATE jobs SET status='failed',finished_at=?,error=? WHERE id=?",
                       (now(), str(exc), job["id"]))
        log("job_failed", str(exc), job["project"])
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Process at most one job")
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--project", type=str, default=None, help="Restrict to one project (no project hopping)")
    args = parser.parse_args()
    initialize()
    if args.once:
        run_one(args.project)
        return
    while True:
        if not run_one(args.project):
            time.sleep(max(5, args.interval))


if __name__ == "__main__":
    main()

