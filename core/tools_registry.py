"""Tools registry — easily add/remove Quick Launch shortcuts."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_CONFIG = ROOT / "config" / "tools.json"


def load_tools():
    """Load tools from config, return only those that exist on disk."""
    if TOOLS_CONFIG.exists():
        with open(TOOLS_CONFIG) as f:
            all_tools = json.load(f)
    else:
        all_tools = get_default_tools()

    available = []
    for tool in all_tools:
        path = Path(tool["path"]).expanduser()
        if path.exists():
            available.append(tool)
    return available


def get_default_tools():
    """Default tool shortcuts — customize by editing tools.json."""
    home = Path.home()
    return [
        {
            "name": "SavvyHomeForge",
            "path": "~/Documents/Codex/2026-07-17/referenced-chatgpt-conversation-this-is-untrusted/SavvyHomeForge/SavvyHomeForge.app",
            "type": "app",
        },
        {"name": "SavvyHub", "path": str(ROOT), "type": "streamlit", "script": "app.py"},
        {
            "name": "GovCon Dashboard",
            "path": str(home / "GovCon_Consolidated" / "govcon_pipeline"),
            "type": "streamlit",
            "script": "app/dashboard.py",
        },
    ]


def launch_tool(tool):
    """Open a tool (app or streamlit)."""
    path = Path(tool["path"]).expanduser()
    if not path.exists():
        return {"ok": False, "error": f"Tool path not found: {path}"}

    try:
        if tool["type"] == "app":
            subprocess.Popen(["open", str(path)])
        elif tool["type"] == "streamlit":
            script = tool.get("script", "app.py")
            subprocess.Popen(["streamlit", "run", str(path / script)])
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def save_tools_config(tools):
    """Save custom tool list to config."""
    TOOLS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with open(TOOLS_CONFIG, "w") as f:
        json.dump(tools, f, indent=2)


if __name__ == "__main__":
    import json

    tools = load_tools()
    print(json.dumps(tools, indent=2))
