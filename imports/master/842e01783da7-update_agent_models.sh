#!/usr/bin/env bash
# ============================================================
# Updates agent_supervisor.sh's job->model mapping to match your
# ACTUAL Ollama models (confirmed from Mac Pro's `ollama list`).
# Run on Mac Pro now. Re-run on Mac Air / NucBox once you send me
# their model lists (mapping may need to differ per machine).
# Run once per machine: bash update_agent_models.sh
# Idempotent — safe to re-run.
# ============================================================
set -e
SUP="$HOME/.sovereign/agent_supervisor.sh"

if [[ ! -f "$SUP" ]]; then
  echo "❌ $SUP not found — run the agent installer first."
  exit 1
fi

echo "→ Patching job→model mapping in $SUP ..."
python3 - "$SUP" << 'PY'
import re, sys
path = sys.argv[1]
content = open(path).read()

old_block = re.search(r'case "\$JOB_TYPE" in.*?esac', content, re.S)
if not old_block:
    print("⚠️  Couldn't find the case block — leaving file untouched, patch by hand.")
    sys.exit(0)

new_block = '''case "$JOB_TYPE" in
  quick)       export OLLAMA_MODEL="llama3.2:3b" ;;       # fastest, confirmed on Mac Pro
  coding)      export OLLAMA_MODEL="phi4:latest" ;;        # good default, cheaper than 32b
  deep-coding) export OLLAMA_MODEL="qwen2.5-coder:32b" ;;  # heaviest, escalation only
  vision)      export OLLAMA_MODEL="llama3.2-vision:latest" ;;
  thinking)    export OLLAMA_MODEL="deepseek-r1:14b" ;;    # deepseek-r1:8b also available, lighter
  *)           export OLLAMA_MODEL="phi4:latest" ;;
esac'''

content = content[:old_block.start()] + new_block + content[old_block.end():]
open(path, "w").write(content)
print("✅ Updated.")
PY

echo ""
echo "Mapping now (confirmed against Mac Pro's ollama list):"
echo "  quick        -> llama3.2:3b"
echo "  coding       -> phi4:latest"
echo "  deep-coding  -> qwen2.5-coder:32b"
echo "  vision       -> llama3.2-vision:latest"
echo "  thinking     -> deepseek-r1:14b"
echo ""
echo "⚠️  'quick' jobs dispatch to the NucBox by design — llama3.2:3b is only"
echo "   confirmed on Mac Pro so far. Send me 'ollama list' from the NucBox and"
echo "   Mac Air once you're back online and I'll split this per-node if needed."
echo ""
echo "Also on Mac Pro, not mapped to a job type: nomic-embed-text (embeddings —"
echo "   likely already feeding ChromaDB, not a chat model) and deepseek-r1:8b /"
echo "   qwen3:4b-instruct (lighter alternates if 14b or phi4 feel slow)."
