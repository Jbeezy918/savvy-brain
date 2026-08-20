#!/bin/zsh
# Start Agent Zero — boots Colima + container if needed, then opens browser.
# Logs to ~/agent_zero/start.log

set -u
LOG=~/agent_zero/start.log
mkdir -p ~/agent_zero
exec > >(tee -a "$LOG") 2>&1
echo ""
echo "=== $(date '+%Y-%m-%d %H:%M:%S') Start Agent Zero ==="

# PATH for double-click launches (Finder doesn't load your shell rc)
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

URL="http://localhost:50001"
CONTAINER="agent-zero"

# 1. Colima
if ! colima status >/dev/null 2>&1; then
  echo "→ Colima down, starting..."
  colima start || { echo "✗ colima start failed"; read -k1 "?Press any key to close..."; exit 1; }
else
  echo "✓ Colima already running"
fi

# 2. Container
state=$(docker inspect -f '{{.State.Status}}' "$CONTAINER" 2>/dev/null || echo "missing")
case "$state" in
  running) echo "✓ $CONTAINER already running" ;;
  exited|created|paused) echo "→ Starting $CONTAINER ($state)..."; docker start "$CONTAINER" ;;
  missing)  echo "✗ Container '$CONTAINER' doesn't exist — recreate it manually"; read -k1 "?Press any key to close..."; exit 1 ;;
  *)        echo "? Unknown state: $state — trying start anyway"; docker start "$CONTAINER" ;;
esac

# 3. Wait for port
echo -n "→ Waiting for $URL "
for i in {1..30}; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
  if [[ "$code" == "200" || "$code" == "302" || "$code" == "401" ]]; then
    echo " ✓ ($code)"
    break
  fi
  echo -n "."
  sleep 1
  [[ $i -eq 30 ]] && { echo " ✗ timeout"; read -k1 "?Press any key to close..."; exit 1; }
done

# 4. Open browser
open "$URL"
echo "✓ Opened $URL"

# Auto-close Terminal window after 2s
sleep 2
osascript -e 'tell application "Terminal" to close (every window whose name contains "Start Agent Zero")' &>/dev/null &
exit 0
