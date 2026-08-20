#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json

ROOT = Path.home() / "AI/AI1"
RAW = ROOT / "opportunities/raw"
EXPIRED = ROOT / "opportunities/expired"
RAW.mkdir(parents=True, exist_ok=True)
EXPIRED.mkdir(parents=True, exist_ok=True)

f = sorted(RAW.glob("sam_live_*.json"))[-1]
data = json.loads(f.read_text())
items = data.get("opportunitiesData", [])
now = datetime.now().astimezone()

for item in items:
    notice = item.get("noticeId", "no_notice")
    deadline = item.get("responseDeadLine", "")
    active = not deadline or datetime.fromisoformat(deadline).astimezone() >= now

    text = f"""Title: {item.get('title','')}
Notice: {notice}
Deadline: {deadline}
Agency: {item.get('fullParentPathName','')}
Type: {item.get('type','')}
NAICS: {item.get('naicsCode','')}
Set Aside: {item.get('typeOfSetAsideDescription','')}
Office: {item.get('officeAddress',{})}
Link: {item.get('uiLink','')}
Attachments: {len(item.get('resourceLinks') or [])}
Resource Links:
{chr(10).join(item.get('resourceLinks') or [])}
Source: SAM.gov
"""

    out = (RAW if active else EXPIRED) / f"sam_{notice}.txt"
    out.write_text(text)
    print(("ACTIVE" if active else "EXPIRED") + ": " + str(out))
