# SavvyHub Memory

## Current State
- Location: ~/Projects/SavvyHub
- Stack: Python/Streamlit/SQLite, local-only
- Status: v1 live-tested, awaiting real data import
- One schema fix was caught and fixed: accounts must be unique per (provider+email), not globally

## How to Run
\`\`\`bash
cd ~/Projects/SavvyHub
streamlit run app.py
\`\`\`

## Next Steps
- Import real chat exports via the Import page
- Monitor Grok/Perplexity exports (no stable bulk-export format yet — use generic "Other" path)
