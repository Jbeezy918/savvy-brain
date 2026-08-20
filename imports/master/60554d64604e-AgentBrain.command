#!/bin/bash
# Managed by Savvy Factory. Re-running the control-center builder may update this file.
set -euo pipefail
SOURCE='/Users/joebudds/Desktop/Cleaned_Work/Misc/Red Flash Drive/AgentBrain'
[ -d "$SOURCE" ] || { echo "Missing tool folder: $SOURCE"; read -r -p "Press Return..." _; exit 1; }
cd "$SOURCE"
export SAVVY_OLLAMA_ENDPOINTS="${SAVVY_OLLAMA_ENDPOINTS:-http://127.0.0.1:11434,http://192.168.68.102:11434}"
exec '/Users/joebudds/Desktop/Cleaned_Work/Misc/Red Flash Drive/AgentBrain/.venv-savvy-py312/bin/python' '/Users/joebudds/Desktop/Cleaned_Work/Misc/Red Flash Drive/AgentBrain/main.py'
