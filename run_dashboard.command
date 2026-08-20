#!/bin/zsh
set -e
SCRIPT_DIR="${0:A:h}"
exec "$SCRIPT_DIR/.venv/bin/streamlit" run "$SCRIPT_DIR/dashboard/app.py"
