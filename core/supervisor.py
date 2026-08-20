"""
Process supervisor for per-project workers.
Manages start/stop/restart of bounded worker processes.
"""

import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from threading import Thread

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.storage import connect, initialize

logger = logging.getLogger("supervisor")


class WorkerSupervisor:
    """Manages worker processes for each enabled project."""

    def __init__(self):
        self.workers = {}  # {project: {"pid": int, "enabled": bool}}
        self.log_dir = ROOT / "logs"
        self.log_dir.mkdir(exist_ok=True)

    def load_projects(self):
        """Scan ideas/ folder and load brain.json for each."""
        projects = {}
        ideas_dir = ROOT / "ideas"
        if ideas_dir.exists():
            for proj_dir in ideas_dir.iterdir():
                if not proj_dir.is_dir():
                    continue
                brain_file = proj_dir / "brain.json"
                if brain_file.exists():
                    try:
                        with open(brain_file) as f:
                            config = json.load(f)
                            projects[proj_dir.name] = {
                                "enabled": config.get("enabled", False),
                                "model": config.get("model", "llama3.2"),
                                "folder": proj_dir,
                            }
                    except Exception as e:
                        logger.warning(f"Failed to load {brain_file}: {e}")
        return projects

    def get_worker_pid(self, project: str):
        """Check if a worker for this project is running."""
        try:
            result = subprocess.run(
                ["pgrep", "-f", f"worker.py.*--project.*{project}"],
                capture_output=True, text=True, timeout=2
            )
            pids = [int(x) for x in result.stdout.strip().split('\n') if x.isdigit()]
            return pids[0] if pids else None
        except Exception as e:
            logger.warning(f"Failed to check PID for {project}: {e}")
            return None

    def track_restart(self, project: str):
        """Track restart event for crash-loop detection."""
        try:
            db = connect()
            db.execute(
                "INSERT INTO worker_restarts (project, restarted_at) VALUES (?, ?)",
                (project, datetime.now().isoformat())
            )
            db.commit()
            # Count restarts in last 10 minutes
            result = db.execute(
                "SELECT COUNT(*) as count FROM worker_restarts WHERE project=? AND restarted_at > datetime('now', '-10 minutes')",
                (project,)
            ).fetchone()
            restart_count = result["count"] if result else 0
            if restart_count >= 5:
                logger.warning(f"CRASH LOOP DETECTED: {project} restarted {restart_count} times in 10 min")
                self._notify_crash_loop(project, restart_count)
            return restart_count
        except Exception as e:
            logger.debug(f"Failed to track restart for {project}: {e}")
            return 0

    def _notify_crash_loop(self, project: str, count: int):
        """Send alert via Beezy if crash-loop detected."""
        try:
            import urllib.request, json
            url = "http://localhost:6789/notify"
            payload = json.dumps({"message": f"⚠️ {project} crashed {count}x in 10 min"}).encode()
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=3)
        except Exception as e:
            logger.debug(f"Failed to send Beezy alert: {e}")

    def start_worker(self, project: str):
        """Start a worker process for one project."""
        pid = self.get_worker_pid(project)
        if pid:
            logger.info(f"Worker for {project} already running (PID {pid})")
            return pid

        self.track_restart(project)  # Record this start/restart
        log_file = self.log_dir / f"worker_{project}.log"
        try:
            proc = subprocess.Popen(
                [
                    str(ROOT / ".venv" / "bin" / "python3"),
                    str(ROOT / "agents" / "worker.py"),
                    "--project", project,
                ],
                stdout=open(log_file, "a"),
                stderr=subprocess.STDOUT,
                cwd=str(ROOT),
            )
            logger.info(f"Started worker for {project}: PID {proc.pid}")
            self.workers[project] = {"pid": proc.pid, "enabled": True}
            return proc.pid
        except Exception as e:
            logger.error(f"Failed to start worker for {project}: {e}")
            return None

    def stop_worker(self, project: str):
        """Stop a worker process for one project."""
        pid = self.get_worker_pid(project)
        if not pid:
            logger.info(f"No worker running for {project}")
            return

        try:
            subprocess.run(["kill", str(pid)], timeout=5)
            logger.info(f"Stopped worker for {project}: PID {pid}")
            self.workers[project] = {"pid": None, "enabled": False}
        except Exception as e:
            logger.error(f"Failed to stop worker for {project}: {e}")

    def sync_workers(self):
        """Ensure running workers match enabled projects; restart any that died."""
        projects = self.load_projects()

        for project, config in projects.items():
            pid = self.get_worker_pid(project)
            if config["enabled"] and not pid:
                logger.info(f"{project}: enabled but not running, starting...")
                self.start_worker(project)
            elif not config["enabled"] and pid:
                logger.info(f"{project}: disabled but running, stopping...")
                self.stop_worker(project)
            elif config["enabled"] and pid:
                logger.debug(f"{project}: enabled and running (PID {pid})")

    def status(self):
        """Return current status of all workers."""
        projects = self.load_projects()
        status_obj = {
            "timestamp": datetime.now().isoformat(),
            "workers": {}
        }
        try:
            db = connect()
        except Exception:
            db = None

        for project, config in projects.items():
            pid = self.get_worker_pid(project)
            restart_count = 0
            if db:
                try:
                    result = db.execute(
                        "SELECT COUNT(*) as count FROM worker_restarts WHERE project=? AND restarted_at > datetime('now', '-10 minutes')",
                        (project,)
                    ).fetchone()
                    restart_count = result["count"] if result else 0
                except Exception:
                    restart_count = 0

            status_obj["workers"][project] = {
                "enabled": config["enabled"],
                "running": pid is not None,
                "pid": pid,
                "model": config["model"],
                "restarts_10m": restart_count,
                "status": "⚠️ crash-loop" if restart_count >= 5 else ("🟢 running" if pid else "⚪ idle"),
            }
        return status_obj

    def watch_loop(self, interval=30):
        """Continuously watch worker status and restart as needed."""
        logger.info(f"Supervisor watch loop starting (interval={interval}s)")
        initialize()
        while True:
            try:
                self.sync_workers()
            except Exception as e:
                logger.error(f"Watch loop error: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="Print current status")
    parser.add_argument("--start", type=str, help="Start worker for PROJECT")
    parser.add_argument("--stop", type=str, help="Stop worker for PROJECT")
    parser.add_argument("--watch", action="store_true", help="Run watch loop")
    parser.add_argument("--interval", type=int, default=30, help="Watch interval (seconds)")
    args = parser.parse_args()

    supervisor = WorkerSupervisor()

    if args.status:
        print(json.dumps(supervisor.status(), indent=2))
    elif args.start:
        supervisor.start_worker(args.start)
    elif args.stop:
        supervisor.stop_worker(args.stop)
    elif args.watch:
        supervisor.watch_loop(args.interval)
    else:
        parser.print_help()
