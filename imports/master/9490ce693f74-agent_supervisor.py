#!/usr/bin/env python3
"""
Agent Supervisor (macOS, zsh-friendly)
- Keeps agents alive (Jenny, Luna, Bob, Lexi, Demo, Butler, Ava)
- Auto-restarts on crash/hang
- Syncs Jenny-led updates (shared version file)
- Ensures earnings monitor is running
- Voice alerts + log file
"""

import os, sys, time, json, signal, shutil, glob, subprocess
from pathlib import Path
from datetime import datetime

# ==== CONFIG ==============================================================
HOME = Path.home()
DOCS = HOME / "Documents"
VENVPY = HOME / ".agents_venv" / "bin" / "python3"
LOG = Path("/tmp/agent_supervisor.log")

AGENTS = ["Jenny", "Luna", "Bob", "Lexi", "Demo", "Butler", "Ava"]

# Where each agent lives ( *_App_Pack_v4 )
def agent_dir(name:str)->Path:
    # Prefer direct match, fallback to case-insensitive find
    d = DOCS / f"{name}_App_Pack_v4"
    if d.exists(): return d
    hits = list(DOCS.rglob(f"{name}_App_Pack_v4"))
    return hits[0] if hits else d  # may not exist

# Possible entrypoints per agent (first match wins)
ENTRY_CANDIDATES = ["jenny.py","luna.py","bob.py","lexi.py","demo.py","butler.py","ava.py","main.py","app.py","agent.py","simple_jenny.py"]

# Shared update/version (Jenny is the source of truth)
SHARED_UPDATES_DIR = HOME / "Agents_Shared" / "updates"
SHARED_VERSION = SHARED_UPDATES_DIR / "version.json"  # {"core_version":"2025-09-05T10:00:00Z"}

# Per-agent version stamp (simple file in their folder)
def agent_version_file(name:str)->Path:
    return agent_dir(name) / ".core_version"

# Earnings monitor file you created earlier
EARN_MONITOR = HOME / "monitor_earnings.py"

# How often to loop
INTERVAL_SEC = 20
# ========================================================================

def say(msg:str):
    try:
        subprocess.run(["say", msg], check=False)
    except Exception:
        pass

def log(msg:str):
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line)
    print(line, end="")

def is_running(pattern:str)->bool:
    try:
        out = subprocess.run(["pgrep","-fl", pattern], capture_output=True, text=True)
        return out.returncode==0 and any(pattern in L for L in out.stdout.splitlines())
    except Exception:
        return False

def find_entrypoint(name:str)->Path|None:
    d = agent_dir(name)
    if not d.exists(): return None
    # search shallow first for speed
    for cand in ENTRY_CANDIDATES:
        for p in [*d.glob(cand), *d.rglob(cand)]:
            return p
    return None

def start_agent(name:str):
    ep = find_entrypoint(name)
    if not ep:
        log(f"❌ {name}: entrypoint not found in {agent_dir(name)}")
        return
    out = Path(f"/tmp/{name.lower()}.out")
    err = Path(f"/tmp/{name.lower()}.err")
    env = os.environ.copy()
    # ensure shared core on path if present
    shared_core = HOME / "Agents_Shared" / "core"
    if shared_core.exists():
        env["PYTHONPATH"] = f"{shared_core}:{env.get('PYTHONPATH','')}"
    cmd = [str(VENVPY), "-u", str(ep)]
    with open(out, "ab") as fo, open(err, "ab") as fe:
        subprocess.Popen(cmd, stdout=fo, stderr=fe, stdin=subprocess.DEVNULL, env=env)
    log(f"🚀 Started {name} -> {ep}")

def stop_agent(name:str):
    # gentle stop by pattern
    pat = f"{name.lower()}.py"
    try:
        subprocess.run(["pkill","-f", pat], check=False)
        log(f"🛑 Stopped {name}")
    except Exception as e:
        log(f"⚠️ Stop {name} error: {e}")

def agent_pidlines(name:str)->list[str]:
    try:
        pat = f"{name.lower()}.py"
        out = subprocess.run(["pgrep","-fl", pat], capture_output=True, text=True)
        return [L for L in out.stdout.splitlines() if pat in L]
    except Exception:
        return []

def touch(path:Path, content:str=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path,"w") as f: f.write(content)

def current_shared_version()->str:
    if SHARED_VERSION.exists():
        try:
            return json.loads(SHARED_VERSION.read_text()).get("core_version","0")
        except Exception:
            return "0"
    return "0"

def read_agent_version(name:str)->str:
    vf = agent_version_file(name)
    if vf.exists():
        try: return vf.read_text().strip()
        except Exception: return "0"
    return "0"

def write_agent_version(name:str, version:str):
    touch(agent_version_file(name), version)

def needs_update(name:str)->bool:
    return current_shared_version() != "0" and read_agent_version(name) != current_shared_version()

def sync_update(name:str):
    """Lightweight sync flag: if shared version changed, restart agent and stamp local version."""
    if not needs_update(name): return False
    stop_agent(name)
    write_agent_version(name, current_shared_version())
    start_agent(name)
    log(f"🔄 {name} updated to {current_shared_version()}")
    say(f"{name} updated")
    return True

def ensure_monitor():
    pat = "monitor_earnings.py"
    if not EARN_MONITOR.exists():
        return
    if not is_running(pat):
        with open("/tmp/earnwatch.out","ab") as fo, open("/tmp/earnwatch.err","ab") as fe:
            subprocess.Popen([str(VENVPY), str(EARN_MONITOR)],
                             stdout=fo, stderr=fe, stdin=subprocess.DEVNULL)
        log("📈 earnings_monitor started")
        try: say("Earnings monitor is active")
        except: pass

def announce_twenty():
    # cheap scan for [ALERT] or cha-ching in monitor logs
    path = Path("/tmp/earnwatch.out")
    if path.exists():
        try:
            tail = path.read_text(errors="ignore")[-2000:]
            if "First $20" in tail or "hit twenty dollars" in tail:
                say("Cha-ching milestone detected")
        except: pass

def status_line(name:str)->str:
    pids = agent_pidlines(name)
    running = "RUNNING" if pids else "STOPPED"
    pid = pids[0].split(" ",1)[0] if pids else "-"
    # peek last log line
    outp = Path(f"/tmp/{name.lower()}.out")
    last = ""
    if outp.exists():
        try:
            last = [l for l in outp.read_text(errors="ignore").splitlines() if l.strip()][-1][-80:]
        except: pass
    return f"{name:7} {running:8} pid={pid:>6} v={read_agent_version(name)} | {last}"

def bootstrap():
    LOG.unlink(missing_ok=True)
    log("🛠️ Agent Supervisor starting…")
    ensure_monitor()
    # Ensure Jenny runs first
    if not agent_pidlines("Jenny"):
        start_agent("Jenny")
        # Stamp Jenny version to shared if missing
        if not SHARED_VERSION.exists():
            v = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            SHARED_UPDATES_DIR.mkdir(parents=True, exist_ok=True)
            SHARED_VERSION.write_text(json.dumps({"core_version": v}, indent=2))
            write_agent_version("Jenny", v)
            log(f"📦 Initialized shared core_version={v}")

def main():
    bootstrap()
    while True:
        # keep earnings monitor alive
        ensure_monitor()
        announce_twenty()

        # If Jenny has newer version, others should follow
        shared_v = current_shared_version()

        for name in AGENTS:
            # Start if not running and entry exists
            if not agent_pidlines(name):
                ep = find_entrypoint(name)
                if ep:
                    start_agent(name)
                else:
                    # only warn for agents that truly should exist
                    log(f"… waiting for {name} (no entrypoint yet)")

            # Sync updates (including Jenny – stamps her local file too)
            if shared_v != "0":
                sync_update(name)

            # Print status
            log(status_line(name))

        time.sleep(INTERVAL_SEC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Supervisor stopped by user.")
        sys.exit(0)ß