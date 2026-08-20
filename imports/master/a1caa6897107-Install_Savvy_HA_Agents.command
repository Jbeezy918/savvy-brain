#!/bin/bash
set -e

APP_DIR="$HOME/Desktop/Savvy_HA_Agents_v1"
INSTALLER_DIR="$APP_DIR/Installers"
ZIP_NAME="Savvy_HA_Agents_v1.zip"

mkdir -p "$APP_DIR" "$INSTALLER_DIR"

if [ -f "$HOME/Downloads/$ZIP_NAME" ]; then
    unzip -o "$HOME/Downloads/$ZIP_NAME" -d "$HOME/Desktop"
elif [ -f "$HOME/Desktop/$ZIP_NAME" ]; then
    unzip -o "$HOME/Desktop/$ZIP_NAME" -d "$HOME/Desktop"
fi

cat << 'PYTHON' > "$APP_DIR/install_token.py"
#!/usr/bin/env python3

import getpass
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

APP_DIR = Path.home() / "Desktop" / "Savvy_HA_Agents_v1"
ENV_FILE = APP_DIR / ".env"
HA_URL = "http://192.168.68.110:8123"

DEFAULTS = {
    "HA_URL": HA_URL,
    "OLLAMA_URL": "http://192.168.68.100:11434",
    "OLLAMA_MODEL": "qwen2.5:7b",
    "BUILDER_MODEL": "qwen2.5-coder:32b",
    "DRY_RUN": "true",
}

AGENT_PROMPT = """
You are Savvy Hub, Joe's Home Assistant orchestrator.

Route requests to:
1. Builder: dashboards, automations, YAML, scenes, scripts and integrations.
2. Guardian: health monitoring, unavailable devices, batteries, logs and recovery.
3. Savvy Hub: conversation, approvals, routing and final reporting.

Never directly edit Home Assistant .storage files.
Validate all services and entity IDs before execution.
Require approval before deletion, restarting Home Assistant, changing integrations,
removing devices, modifying security settings or performing destructive actions.
Report failures honestly and verify every completed action.
""".strip()


def read_env():
    values = {}

    if not ENV_FILE.exists():
        return values

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


def write_env(token):
    values = read_env()
    values.update(DEFAULTS)
    values["HA_TOKEN"] = token

    content = "\n".join(
        f"{key}={value}"
        for key, value in values.items()
    ) + "\n"

    ENV_FILE.write_text(content, encoding="utf-8")
    os.chmod(ENV_FILE, 0o600)

    prompt_file = APP_DIR / "savvy_hub_prompt.txt"
    prompt_file.write_text(AGENT_PROMPT + "\n", encoding="utf-8")


def verify(token):
    request = urllib.request.Request(
        f"{HA_URL}/api/",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return True, data.get("message", "API connected")

    except urllib.error.HTTPError as exc:
        return False, f"Home Assistant returned HTTP {exc.code}"

    except urllib.error.URLError as exc:
        return False, f"Could not reach Home Assistant: {exc.reason}"


def main():
    APP_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Savvy HA Agent Setup")
    print("=" * 60)
    print(f"Project folder: {APP_DIR}")
    print(f"Token file: {ENV_FILE}")
    print("\nYour token will not appear while you paste it.")

    token = getpass.getpass(
        "\nPaste your Home Assistant long-lived access token: "
    ).strip()

    if len(token) < 20:
        raise SystemExit("ERROR: The token is missing or too short.")

    write_env(token)

    success, result = verify(token)

    if success:
        print("\nSUCCESS: Home Assistant accepted the token.")
        print(result)
    else:
        print("\nThe token was saved, but verification failed.")
        print(result)

    print(f"\nToken stored securely at:\n{ENV_FILE}")
    print(f"\nAgent prompt stored at:\n{APP_DIR / 'savvy_hub_prompt.txt'}")


if __name__ == "__main__":
    main()
PYTHON

chmod +x "$APP_DIR/install_token.py"
python3 "$APP_DIR/install_token.py"

mv "$0" "$INSTALLER_DIR/Install_Savvy_HA_Agents.command"

echo
echo "Installer put away at:"
echo "$INSTALLER_DIR/Install_Savvy_HA_Agents.command"
echo
read -p "Press Return to close..."
