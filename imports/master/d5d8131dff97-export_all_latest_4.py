#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import json

ROOT = Path.home() / "AI/AI1"
RAW = ROOT / "opportunities/raw"
EXPIRED = ROOT / "opportunities/expired"
RAW.mkdir(parents=True, exist_ok=True)
EXPIRED.mkdir(parents=True, exist_ok=True)

now = datetime.now().astimezone()
seen = set()

for f in sorted(RAW.glob("sam_live_*.json"))[-20:]:
    data = json.loads(f.read_text(errors="ignore"))
    for item in data.get("opportunitiesData", []):
        notice = item.get("noticeId", "no_notice")
        if notice in seen:
            continue
        seen.add(notice)

        deadline = item.get("responseDeadLine", "")
        active = not deadline or datetime.fromisoformat(deadline).astimezone() >= now
        links = item.get("resourceLinks") or []

        text = f"""Title: {item.get('title','')}
Notice: {notice}
Deadline: {deadline}
Agency: {item.get('fullParentPathName','')}
Type: {item.get('type','')}
NAICS: {item.get('naicsCode','')}
Set Aside: {item.get('typeOfSetAsideDescription','')}
Office: {item.get('officeAddress',{})}
Link: {item.get('uiLink','')}
Attachments: {len(links)}
Resource Links:
{chr(10).join(links)}
Source: SAM.gov
"""

        out = (RAW if active else EXPIRED) / f"sam_{notice}.txt"
        out.write_text(text)
        print(("ACTIVE" if active else "EXPIRED") + ": " + str(out))

print(f"\nExported unique notices: {len(seen)}")
