# Savvy Suite Control Center Result

- Control root: `/Users/joebudds/Desktop/Savvy_Suite`
- Tools: **16**
- Models: **7**
- Status: **control_ready=10, environment_install_failed=1, folder_only_safety=1, inferred_launcher_ready=1, needs_entrypoint_review=3**

| Tool | Status | Selected launcher | Environment |
|---|---|---|---|
| Savvy Consolidator | control_ready | run.command | yes |
| SavvyTube OS | control_ready | app/dashboard.py | no |
| Savvy App Forge | control_ready | start.command | no |
| Savvy Home Forge | control_ready | start.command | no |
| Savvy Market Forge | control_ready | start.command | no |
| Savvy Site Forge | control_ready | start.command | no |
| Savvy Tube Forge | control_ready | start.command | no |
| SOP Sync | control_ready | Launch_SOPSync.command | no |
| GovCon HQ | control_ready | launch.command | yes |
| GovCon Micro Tools | control_ready | app.py | no |
| AI Assistant | needs_entrypoint_review | review needed | no |
| Career Assistant AI | needs_entrypoint_review | review needed | no |
| Career Creator | needs_entrypoint_review | review needed | no |
| Home Assistant Agent | inferred_launcher_ready | agent_builder.py | no |
| Mac Cleanup Tools | folder_only_safety | review needed | no |
| AgentBrain | environment_install_failed | main.py | yes |

## Items requiring review

### AI Assistant — needs_entrypoint_review

- Source: `/Users/joebudds/Desktop/AI_assistant`
- External imports observed: docx2txt, psycopg2, pypdf
- Entrypoint candidate: `import_resumes.py` (score 115)
- Entrypoint candidate: `pipeline_compiler.py` (score 115)
- Entrypoint candidate: `backend/memory_extractor.py` (score 100)
- Entrypoint candidate: `backend/system_sweep.py` (score 100)
- Entrypoint candidate: `pipeline_db.py` (score 15)
- Entrypoint candidate: `router.py` (score 15)

### Career Assistant AI — needs_entrypoint_review

- Source: `/Users/joebudds/Desktop/Career_Assistant_AI`
- External imports observed: docx, duckduckgo_search, fitz, getpass, google, google_auth_oauthlib, imaplib, keyring, pandas
- Entrypoint candidate: `auth_helper.py` (score 115)
- Entrypoint candidate: `extract_tokens.py` (score 115)
- Entrypoint candidate: `parser.py` (score 115)
- Entrypoint candidate: `watchdog.py` (score 115)
- Entrypoint candidate: `consolidator.py` (score 15)
- Entrypoint candidate: `run_watchdog.py` (score 15)

### Career Creator — needs_entrypoint_review

- Source: `/Users/joebudds/Desktop/career_creator`
- Entrypoint candidate: `init_rapport_tuning.py` (score 115)
- Entrypoint candidate: `job_analyzer.py` (score 115)
- Entrypoint candidate: `update_pipeline_logic.py` (score 115)

### Mac Cleanup Tools — folder_only_safety

- Source: `/Users/joebudds/Desktop/Mac_Cleanup_Tools`
- External imports observed: PyPDF2, cryptography, difflib, docx, pandas, streamlit
- Entrypoint candidate: `Mac_Cleanup_Quarantine_20260519_123419/aie_v3.py` (score 35)

### AgentBrain — environment_install_failed

- Source: `/Users/joebudds/Desktop/Cleaned_Work/Misc/Red Flash Drive/AgentBrain`
- Environment: Environment created, but package installation failed:
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pydantic-core
Failed to build pydantic-core

[notice] A new release of pip is available: 26.1.1 -> 26.1.2
[notice] To update, run: /Users/joebudds/Desktop/Cleaned_Work/Misc/Red Flash Drive/AgentBrain/.venv/bin/python -m pip install --upgrade pip
error: failed-wheel-build-for-install

× Failed to build installable wheels for some pyproject.toml based projects
╰─> pydantic-core
- External imports observed: agents, api, fastapi, orchestrator, pydantic, requests, twilio, uvicorn
- Entrypoint candidate: `main.py` (score 205)
- Entrypoint candidate: `api/steward_api.py` (score 135)
- Entrypoint candidate: `Clipboard_setup_nfirst of webby/clipboard_sync_mac.py` (score 100)
- Entrypoint candidate: `Clipboard_setup_nfirst of webby/SavvyTech_Business_Complete/02_OrderBot/orderbot_demo/review_poster.py` (score 100)
- Entrypoint candidate: `Clipboard_setup_nfirst of webby/SavvyTech_Business_Complete/02_OrderBot/orderbot_demo/sms_handler.py` (score 100)

## Model routes

- **fast:** llama3.2:3b (3.2B) @ http://127.0.0.1:11434
- **standard:** qwen2.5-coder:32b (32.8B) @ http://127.0.0.1:11434
- **reasoning:** deepseek-r1:14b (14.8B) @ http://127.0.0.1:11434
- **coding:** qwen2.5-coder:32b (32.8B) @ http://127.0.0.1:11434
- **vision:** llama3.2-vision:latest (10.7B) @ http://127.0.0.1:11434

## Unreachable model servers

- `http://192.168.68.102:11434`: request failed for http://192.168.68.102:11434/api/tags: <urlopen error timed out>
