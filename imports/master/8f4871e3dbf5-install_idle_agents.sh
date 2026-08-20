#!/usr/bin/env bash
# ============================================================
# IDLE-WORK LAYER — what Titus/Ava do when you don't give them a task
#
# Titus (idle):   finds your most recently active project, copies it (NEVER
#                 touches the original), and keeps building toward completion.
# Ava (idle): audits the most recent work — errors, gaps, security —
#                 no building, no commits to anything real. Matches Ava's
#                 existing audit-only role, doesn't turn it into a builder.
#
# Universal pieces run on any machine (NucBox, Mac). Notifications/voice/
# "welcome back" only apply where there's a screen+speakers (Mac).
#
# Run once per machine: bash install_idle_agents.sh
# Idempotent.
# ============================================================
set -e
SOV="$HOME/.sovereign"
mkdir -p "$SOV/tasks" "$SOV/workspace" "$SOV/logs" "$SOV/checkpoints"
IS_MAC=false
[[ "$(uname)" == "Darwin" ]] && IS_MAC=true

# ---- 1. projects.conf — pre-filled with paths from your own .zshrc, edit freely ----
if [[ ! -f "$SOV/projects.conf" ]]; then
  echo "→ Writing starter projects.conf (edit this — add/remove directories) ..."
  cat << EOF > "$SOV/projects.conf"
# Sovereign idle-work watchlist — one directory per line, # comments ignored.
# Pre-filled from paths seen in your own .zshrc — verify these still exist.
$HOME/AI_SYSTEM
$HOME/HomeHub
$HOME/GOVCON_AI
$HOME/.spark_tracker
EOF
else
  echo "→ projects.conf already exists, leaving it alone."
fi

# ---- 2. idle_dispatcher.sh — universal, runs on whichever machine executes the agent ----
echo "→ Writing idle_dispatcher.sh ..."
cat << 'DISPATCH_EOF' > "$SOV/idle_dispatcher.sh"
#!/usr/bin/env bash
# Runs continuously under agent_supervisor.sh. Each cycle: if there's an
# explicit task queued, run it. Otherwise idle behavior kicks in — different
# per role (Titus builds, Ava audits only).
# Usage: idle_dispatcher.sh <agent-name> [actual-cli-command]
set -uo pipefail

AGENT="$1"
CMD="${2:-$AGENT}"
SOV="$HOME/.sovereign"
TASK_FILE="$SOV/tasks/$AGENT.task"
WORKSPACE_ROOT="$SOV/workspace/$AGENT"
PROJECTS_CONF="$SOV/projects.conf"
LOG_FILE="$SOV/logs/$AGENT.log"
POLL_SECONDS=600

mkdir -p "$SOV/tasks" "$WORKSPACE_ROOT" "$(dirname "$LOG_FILE")"
log() { echo "[$(date '+%F %T')] $*" >> "$LOG_FILE"; }

pick_active_project() {
  [[ -f "$PROJECTS_CONF" ]] || { log "no projects.conf — nothing to scan"; return 1; }
  python3 - "$PROJECTS_CONF" "$WORKSPACE_ROOT" << 'PY'
import sys, os
conf, workspace_root = sys.argv[1], sys.argv[2]
best, best_time = None, -1
with open(conf) as f:
    dirs = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
for d in dirs:
    if not os.path.isdir(d) or d.startswith(workspace_root):
        continue
    latest = -1
    for root, subdirs, files in os.walk(d):
        if ".git" in root:
            continue
        for fn in files:
            try:
                latest = max(latest, os.path.getmtime(os.path.join(root, fn)))
            except OSError:
                pass
    if latest > best_time:
        best_time, best = latest, d
if best:
    print(best)
PY
}

make_safe_copy() {
  local src="$1"
  local name; name=$(basename "$src")
  local dest="$WORKSPACE_ROOT/${name}__copy__$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$dest"
  cp -a "$src/." "$dest/" 2>/dev/null
  touch "$dest/.sovereign-workspace"
  if [[ -d "$dest/.git" ]]; then
    (cd "$dest" && git add -A && git commit -q -m "sovereign: snapshot before $AGENT idle session" 2>/dev/null || true)
  fi
  echo "$dest"
}

write_brief() {
  local dest="$1" brief="$dest/SOVEREIGN_BRIEF.md"
  if [[ "$AGENT" == "titus" ]]; then
    cat << BRIEF > "$brief"
# Sovereign idle task — build
You are working in an isolated COPY at: $dest
The original project was left untouched — do not look for or touch it.
Read every file here until you understand what's being built, then continue
building toward completion. When you finish a meaningful chunk, print a line
starting with "MILESTONE:". When the whole thing is done and ready for Joe's
review, print a line starting with "COMPLETE:".
BRIEF
  else
    cat << BRIEF > "$brief"
# Sovereign idle task — audit only. No building. No commits to anything real.
You are reviewing a disposable COPY at: $dest — the original is untouched.
Find errors, incomplete work, security issues, or style problems.
Print a line starting with "MILESTONE:" for each significant finding.
Print a line starting with "COMPLETE:" with a summary when the audit is done.
BRIEF
  fi
  echo "$brief"
}

while true; do
  if [[ -s "$TASK_FILE" ]]; then
    log "explicit task found, running it"
    task_content=$(cat "$TASK_FILE")
    "$CMD" "$task_content" >> "$LOG_FILE" 2>&1
    : > "$TASK_FILE"
  else
    project=$(pick_active_project || true)
    if [[ -n "$project" ]]; then
      log "idle — picked project: $project"
      copy=$(make_safe_copy "$project")
      brief=$(write_brief "$copy")
      log "working copy: $copy"
      # ASSUMPTION — VERIFY: $CMD is assumed to accept (working-dir, brief-file).
      # If titus/ava's real CLI differs, this is the one line to change.
      "$CMD" "$copy" "$brief" >> "$LOG_FILE" 2>&1
    else
      log "idle — nothing found in projects.conf, sleeping"
    fi
  fi
  sleep "$POLL_SECONDS"
done
DISPATCH_EOF
chmod +x "$SOV/idle_dispatcher.sh"

# ---- Mac-only pieces: notifications, voice, welcome-back, review command ----
if $IS_MAC; then
  echo "→ Mac detected — installing notifications, welcome-back, and agent-review ..."

  cat << 'WATCH_EOF' > "$SOV/agent_watch.sh"
#!/usr/bin/env bash
# Heartbeat + milestone/completion watcher. Runs every 60s via launchd.
source "$HOME/.sovereign_tools.zsh" 2>/dev/null || exit 0
STALE_DIR="$HOME/.sovereign/alerted"
CHECKPOINT_DIR="$HOME/.sovereign/checkpoints"
mkdir -p "$STALE_DIR" "$CHECKPOINT_DIR"

notify() { osascript -e "display notification \"$2\" with title \"$1\"" 2>/dev/null; }

for entry in "${AGENT_REGISTRY[@]}"; do
  IFS=':' read -r name voice cmd <<< "$entry"

  hb="$HOME/.sovereign/heartbeats/$name.hb"
  mark="$STALE_DIR/$name.alerted"
  if [[ -f "$hb" ]]; then
    age=$(( $(date +%s) - $(cat "$hb") ))
    if [[ $age -gt 90 ]]; then
      [[ -f "$mark" ]] || { agent-speak "$name" "$name has gone silent. Heartbeat lost."; notify "$name" "Heartbeat lost"; touch "$mark"; }
    else
      rm -f "$mark"
    fi
  fi

  log="$HOME/.sovereign/logs/$name.log"
  checkpoint="$CHECKPOINT_DIR/$name.lines"
  [[ -f "$log" ]] || continue
  total_lines=$(wc -l < "$log" 2>/dev/null || echo 0)
  last_lines=$(cat "$checkpoint" 2>/dev/null || echo 0)
  if [[ "$total_lines" -gt "$last_lines" ]]; then
    tail -n +"$((last_lines + 1))" "$log" | grep -E "MILESTONE:|COMPLETE:" | while IFS= read -r line; do
      if [[ "$line" == *"COMPLETE:"* ]]; then
        agent-speak "$name" "$name finished a project and is waiting for your approval."
        notify "$name — waiting for approval" "${line#*COMPLETE:}"
      else
        notify "$name — milestone" "${line#*MILESTONE:}"
      fi
    done
  fi
  echo "$total_lines" > "$checkpoint"
done
WATCH_EOF
  chmod +x "$SOV/agent_watch.sh"

  if ! grep -q "IDLE WORK LAYER" "$HOME/.sovereign_tools.zsh" 2>/dev/null; then
cat << 'TOOLS_EOF' >> "$HOME/.sovereign_tools.zsh"

# ============ IDLE WORK LAYER ============
_welcome_back_check() {
  local seen="$HOME/.sovereign/last_seen"
  local now=$(date +%s)
  if [[ -f "$seen" ]]; then
    local gap=$(( now - $(cat "$seen") ))
    if [[ $gap -gt 7200 ]]; then
      local recent
      recent=$(grep -h "COMPLETE:\|MILESTONE:" "$HOME/.sovereign/logs/"*.log 2>/dev/null | tail -3)
      if [[ -n "$recent" ]]; then
        agent-speak titus "Welcome back. Here's what happened while you were away."
        echo "$recent"
      else
        agent-speak titus "Welcome back."
      fi
    fi
  fi
  echo "$now" > "$seen"
}

# Redefines node-check to greet you on return — supersedes the earlier version.
node-check() {
  _welcome_back_check
  if [[ "$1" == "--live" || "$1" == "-l" ]]; then
    bash "$SOVEREIGN_MONITOR"
  elif [[ -f "$SOVEREIGN_STATUS" ]]; then
    cat "$SOVEREIGN_STATUS"
    echo "(cached — updates every 5 min in background; run 'node-check --live' to force a fresh scan)"
  else
    echo "No cached status yet — running first live scan..."
    bash "$SOVEREIGN_MONITOR"
  fi
}

# Points a specific task at an agent instead of letting it go idle-autonomous.
agent-task() {
  local name="$1"; shift
  mkdir -p "$HOME/.sovereign/tasks"
  echo "$*" > "$HOME/.sovereign/tasks/$name.task"
  echo "Task queued for $name — it'll pick this up instead of idle work."
}

# Lists pending idle-work, local and on the NucBox, so you can review before approving.
agent-review() {
  local agent="${1:-titus}"
  local ws="$HOME/.sovereign/workspace/$agent"
  if [[ -d "$ws" ]] && [[ -n "$(ls -A "$ws" 2>/dev/null)" ]]; then
    echo "Local workspaces for $agent:"
    for d in "$ws"/*/; do
      [[ -d "$d" ]] || continue
      echo "--- $d ---"
      (cd "$d" && git log --oneline -5 2>/dev/null)
    done
  fi
  local ip
  ip=$(python3 -c "
import json
try:
    d = json.load(open('$HOME/.sovereign/status.json'))
    for n in d['nodes']:
        if n['name'] == 'Nuk Node Cluster':
            print(n['ip']); break
except Exception:
    pass
")
  if [[ -n "$ip" ]]; then
    echo "Workspaces on NucBox ($ip):"
    ssh -o ConnectTimeout=3 "$ip" "for d in \$HOME/.sovereign/workspace/$agent/*/; do [ -d \"\$d\" ] && echo \"--- \$d ---\" && (cd \"\$d\" && git log --oneline -5 2>/dev/null); done" 2>/dev/null
  fi
  echo ""
  echo "Nothing here auto-merges into your real project — review the diffs above"
  echo "and copy/patch in what you want by hand."
}
TOOLS_EOF
  else
    echo "   agent commands already present, skipping."
  fi

  echo "→ Restarting agent-watch timer to pick up milestone detection ..."
  launchctl unload "$HOME/Library/LaunchAgents/com.savvytech.agentwatch.plist" 2>/dev/null || true
  launchctl load "$HOME/Library/LaunchAgents/com.savvytech.agentwatch.plist" 2>/dev/null || true
fi

echo ""
echo "✅ Idle-work layer installed."
echo ""
echo "⚠️  Two things that need your input:"
echo "   1. Edit ~/.sovereign/projects.conf — confirm those paths still exist,"
echo "      add any others you want scanned."
echo "   2. idle_dispatcher.sh assumes titus/ava accept (working-dir, brief-file)"
echo "      as arguments. If their real CLI is different, that's ONE line to fix —"
echo "      show me the actual command and I'll correct it."
echo ""
echo "To make an agent's supervised process run idle_dispatcher.sh instead of the"
echo "raw command, change its ExecStart / agent_supervisor.sh call from:"
echo "   agent_supervisor.sh titus coding -- titus"
echo "to:"
echo "   agent_supervisor.sh titus coding -- $HOME/.sovereign/idle_dispatcher.sh titus titus"
echo ""
echo "New commands (Mac): agent-task <name> \"do this instead\"  |  agent-review <name>"
