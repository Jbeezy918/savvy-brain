#!/bin/bash
APP="$HOME/Desktop/Tools/SavvyConsolidator"
cd "$APP" || exit 1
"$APP/.venv/bin/python" "$APP/export_env.py"
open "$HOME/Desktop/Savvy Master Library/ENV Exports"
