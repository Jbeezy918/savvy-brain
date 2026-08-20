"""System health monitoring — disk space, logs, restarts, errors."""

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAWD_HOME = Path.home() / "clawd"


def get_disk_health():
    """Check free disk space on home volume."""
    usage = shutil.disk_usage(str(Path.home()))
    free_gb = usage.free / (1024**3)
    used_gb = usage.used / (1024**3)
    total_gb = usage.total / (1024**3)
    return {
        "free_gb": round(free_gb, 1),
        "used_gb": round(used_gb, 1),
        "total_gb": round(total_gb, 1),
        "percent_free": round(100 * free_gb / total_gb, 1),
        "status": "critical" if free_gb < 10 else "warning" if free_gb < 20 else "ok",
    }


def get_log_sizes():
    """Total size of all agent logs."""
    total = 0
    for agent_dir in (CLAWD_HOME / "agents").glob("*/_logs"):
        if agent_dir.exists():
            total += sum(f.stat().st_size for f in agent_dir.rglob("*") if f.is_file())
    return {"total_bytes": total, "total_gb": round(total / (1024**3), 2)}


def get_database_size():
    """Size of savvy_brain.db."""
    db_file = ROOT / "data" / "savvy_brain.db"
    if db_file.exists():
        size_bytes = db_file.stat().st_size
        return {"bytes": size_bytes, "gb": round(size_bytes / (1024**3), 3)}
    return {"bytes": 0, "gb": 0}


def get_worker_health():
    """Status of all project workers: running, restart count, last error."""
    try:
        from core.supervisor import WorkerSupervisor
        supervisor = WorkerSupervisor()
        status = supervisor.status()
        return status["workers"]
    except Exception:
        return {}


def get_health_summary():
    """Full health report."""
    disk = get_disk_health()
    logs = get_log_sizes()
    db = get_database_size()
    workers = get_worker_health()

    return {
        "timestamp": datetime.now().isoformat(),
        "disk": disk,
        "logs": logs,
        "database": db,
        "workers": workers,
        "overall_status": disk["status"],  # disk is the critical bottleneck
    }


if __name__ == "__main__":
    import json

    summary = get_health_summary()
    print(json.dumps(summary, indent=2))
