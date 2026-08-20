#!/bin/bash
# Managed by Savvy Factory. Re-running the control-center builder may update this file.
set -euo pipefail
SOURCE=/Users/joebudds/Desktop/HA_Agent
[ -d "$SOURCE" ] || { echo "Missing tool folder: $SOURCE"; read -r -p "Press Return..." _; exit 1; }
cd "$SOURCE"
export SAVVY_OLLAMA_ENDPOINTS="${SAVVY_OLLAMA_ENDPOINTS:-http://127.0.0.1:11434,http://192.168.68.102:11434}"
exec /Users/joebudds/Desktop/HA_Agent/.venv/bin/python /Users/joebudds/Desktop/HA_Agent/agent_builder.py
