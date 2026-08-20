#!/bin/bash
export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/v22.18.0/bin:$PATH"
export OLLAMA_BASE_URL="http://localhost:11434"
cd "$HOME/SavvyTech_Brain/tools/roundtable"
exec python3 roundtable.py
