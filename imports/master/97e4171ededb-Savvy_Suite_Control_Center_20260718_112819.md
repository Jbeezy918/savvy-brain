# Savvy Suite Control Center Result

- Control root: `/Users/joebudds/Desktop/Savvy_Suite`
- Tools: **16**
- Models: **13**
- Status: **control_ready=11, folder_only_safety=1, inferred_launcher_ready=1, menu_launcher_ready=3**

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
| AI Assistant | menu_launcher_ready | menu (4 actions) | yes |
| Career Assistant AI | menu_launcher_ready | menu (5 actions) | yes |
| Career Creator | menu_launcher_ready | menu (3 actions) | no |
| Home Assistant Agent | inferred_launcher_ready | agent_builder.py | yes |
| Mac Cleanup Tools | folder_only_safety | review needed | no |
| AgentBrain | control_ready | main.py | yes |

## Items requiring review

### Mac Cleanup Tools — folder_only_safety

- Source: `/Users/joebudds/Desktop/Mac_Cleanup_Tools`
- External imports observed: PyPDF2, cryptography, difflib, docx, pandas, streamlit
- Entrypoint candidate: `Mac_Cleanup_Quarantine_20260519_123419/aie_v3.py` (score 35)

## Model routes

- **fast:** llama3.2:3b (3.2B) @ http://127.0.0.1:11434
- **standard:** qwen2.5-coder:32b (32.8B) @ http://127.0.0.1:11434
- **reasoning:** deepseek-r1:32b (32.8B) @ http://192.168.68.102:11434
- **coding:** qwen2.5-coder:32b (32.8B) @ http://127.0.0.1:11434
- **vision:** llama3.2-vision:latest (10.7B) @ http://127.0.0.1:11434
