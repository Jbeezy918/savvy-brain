#!/bin/bash
set -e

APP="$HOME/Desktop/Tools/SavvyConsolidator"
PYTHON="$APP/.venv/bin/python"
MASTER="$HOME/Desktop/Savvy Master Library/Savvy_Master.xlsx"

cat << 'PYEOF' > "$APP/setup_env_export.py"
import re
from pathlib import Path
from openpyxl import load_workbook

master = Path.home() / "Desktop/Savvy Master Library/Savvy_Master.xlsx"
wb = load_workbook(master)
keys = wb["API Keys & Tokens"]

if "ENV Export" in wb.sheetnames:
    del wb["ENV Export"]

env = wb.create_sheet("ENV Export")
env.append([
    "Include", "Project", "Environment", "Variable Name",
    "Full Value", "Provider", "Credential Type",
    "Format Status", "Source File", "Notes"
])

headers = {
    str(cell.value).strip(): index
    for index, cell in enumerate(keys[1], start=1)
}

used = set()

for row in range(2, keys.max_row + 1):
    provider = str(keys.cell(row, headers["Provider"]).value or "").strip()
    credential_type = str(
        keys.cell(row, headers["Credential Type"]).value or ""
    ).strip()
    value = str(keys.cell(row, headers["Full Value"]).value or "").strip()
    source = str(keys.cell(row, headers["Source File"]).value or "").strip()
    variable = str(
        keys.cell(row, headers["Environment Variable"]).value or ""
    ).strip()

    variable = re.sub(r"[^A-Za-z0-9_]+", "_", variable.upper()).strip("_")
    variable = variable or "UNKNOWN_SECRET"

    original = variable
    number = 2
    while variable in used:
        variable = f"{original}_{number}"
        number += 1
    used.add(variable)

    status = "PLAUSIBLE — live test not performed"
    if not value:
        status = "INVALID — empty value"
    elif any(character.isspace() for character in value):
        status = "INVALID — contains whitespace"

    env.append([
        "YES" if not status.startswith("INVALID") else "NO",
        "General",
        "local",
        variable,
        value,
        provider,
        credential_type,
        status,
        source,
        "Set Include to YES or NO, then save workbook."
    ])

env.freeze_panes = "A2"
env.auto_filter.ref = env.dimensions
wb.save(master)

print("ENV Export tab created.")
print(master)
PYEOF

cat << 'PYEOF' > "$APP/export_env.py"
from pathlib import Path
from openpyxl import load_workbook

master = Path.home() / "Desktop/Savvy Master Library/Savvy_Master.xlsx"
output_dir = Path.home() / "Desktop/Savvy Master Library/ENV Exports"
output_file = output_dir / "Savvy_Master.env"

wb = load_workbook(master, data_only=False)
sheet = wb["ENV Export"]

headers = {
    str(cell.value).strip(): index
    for index, cell in enumerate(sheet[1], start=1)
}

lines = [
    "# Savvy Master ENV Export",
    "# Keep private. Never commit this file to Git.",
    "",
]

count = 0

for row in range(2, sheet.max_row + 1):
    include = str(
        sheet.cell(row, headers["Include"]).value or ""
    ).strip().upper()

    if include not in {"YES", "Y", "TRUE", "1"}:
        continue

    variable = str(
        sheet.cell(row, headers["Variable Name"]).value or ""
    ).strip()
    value = str(
        sheet.cell(row, headers["Full Value"]).value or ""
    ).strip()
    status = str(
        sheet.cell(row, headers["Format Status"]).value or ""
    ).strip()

    if not variable or not value or status.startswith("INVALID"):
        continue

    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    lines.append(f'{variable}="{escaped}"')
    count += 1

output_dir.mkdir(parents=True, exist_ok=True)
output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
output_file.chmod(0o600)

print(f"Exported {count} credential(s).")
print(output_file)
PYEOF

cat << 'LAUNCHEOF' > "$HOME/Desktop/Export Savvy ENV.command"
#!/bin/bash
APP="$HOME/Desktop/Tools/SavvyConsolidator"
cd "$APP" || exit 1
"$APP/.venv/bin/python" "$APP/export_env.py"
open "$HOME/Desktop/Savvy Master Library/ENV Exports"
LAUNCHEOF

chmod +x "$HOME/Desktop/Export Savvy ENV.command"

"$PYTHON" "$APP/setup_env_export.py"
open "$MASTER"
