# Savvy Brain

Savvy Brain is a local-first project intelligence workspace. Every project has an independent brief, goals, memory, inbox, assets, outputs, execution interface, and LLM configuration. A shared SQLite index provides search, activity history, and a durable job queue.

The **Talk to Savvy** page supports typed chat, microphone recording, grounded status answers, and spoken replies. macOS speech uses the built-in system voice. Dictation transcription requires `LLM_API_KEY`.

## Start

```bash
cd ~/savvy_brain
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/index_workspace.py
streamlit run dashboard/app.py
```

In a second terminal, start the bounded worker:

```bash
cd ~/savvy_brain
. .venv/bin/activate
python agents/worker.py
```

The default provider is local Ollama at `http://127.0.0.1:11434`. For an OpenAI-compatible endpoint, set `LLM_API_KEY` and optionally `LLM_BASE_URL`. API keys are read from the environment and must never be stored in project files.

## Safety model

Queued agents can read project context and write Markdown proposals only to that project's `outputs/` folder. They do not edit source files, communicate externally, or spend money beyond LLM calls you explicitly configure. Continuous operation requires you to start and supervise the worker.

Outputs can be submitted for review. Approval creates a timestamped official release and updates `releases/current.json`; earlier official versions remain archived for recovery.

## What is not automatic yet

Historical chat exports and external/network documents must be copied or linked into an approved import location before indexing. Savvy Brain does not bypass application permissions or scrape private data. Production-grade 24/7 operation also needs a supervised OS service, budgets, backups, and provider credentials.
