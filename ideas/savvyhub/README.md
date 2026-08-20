# SavvyHub — Personal AI Data Consolidator

SavvyHub is a local-first Streamlit app that imports chat exports from all your AI assistant interactions:
Claude, ChatGPT, Gemini, Grok, Perplexity, Ollama, and others.

All data is stored in a local SQLite database. The "Get My Data" page has one-click links to each provider's official export page.

A Coach module (using local Ollama, privacy-redacted) can analyze communication patterns without sending data anywhere.

## Status
v1 is live-tested and ready for real imports. Schema has been validated; one account-uniqueness fix was applied.

## Running
```bash
cd ~/Projects/SavvyHub
streamlit run app.py
```

Then use the Import page to upload your chat exports.
