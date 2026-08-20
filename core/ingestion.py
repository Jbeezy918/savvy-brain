"""Non-destructive discovery and staging with provenance and SHA-256 deduplication."""
from __future__ import annotations
import hashlib, shutil
import re
from pathlib import Path
from core.storage import ROOT, connect, now

SAFE_NAMES=("savvy","chatgpt","claude","conversations.json")
TEXT={".json",".md",".txt",".csv",".yaml",".yml"}

def preview(item_id: int, limit: int = 5000) -> str:
    with connect() as db: item=db.execute("SELECT source_path FROM ingestion_items WHERE id=?",(item_id,)).fetchone()
    if not item: raise ValueError("Unknown ingestion item")
    path=Path(item["source_path"])
    if path.suffix.lower() not in TEXT: return "Preview is unavailable for this file type. Review its name, type, and size before approval."
    return path.read_text(encoding="utf-8",errors="replace")[:limit]

def decide(item_id: int, action: str, scope_id: str = "master") -> str | None:
    if action not in {"approve","hold","ignore"}: raise ValueError("Invalid review action")
    with connect() as db: item=db.execute("SELECT * FROM ingestion_items WHERE id=?",(item_id,)).fetchone()
    if not item: raise ValueError("Unknown ingestion item")
    if action == "hold":
        with connect() as db: db.execute("UPDATE ingestion_items SET status='review',review_reason='Held for later review',scope_id=? WHERE id=?",(scope_id,item_id))
        return None
    if action == "ignore":
        with connect() as db: db.execute("UPDATE ingestion_items SET status='ignored',review_reason='Ignored by Joe',scope_id=? WHERE id=?",(scope_id,item_id))
        return None
    source=Path(item["source_path"])
    if not source.is_file(): raise FileNotFoundError("The original file is no longer available")
    safe_name=re.sub(r"[^A-Za-z0-9._-]+","_",source.name).strip("._") or f"item-{item_id}"
    if scope_id.startswith("project:"):
        project=scope_id.split(":",1)[1]
        if not project or "/" in project or ".." in project: raise ValueError("Invalid project scope")
        destination=ROOT/"ideas"/project/"imports"/f"{item['sha256'][:12]}-{safe_name}"
    elif scope_id == "master": destination=ROOT/"imports"/"master"/f"{item['sha256'][:12]}-{safe_name}"
    else: raise ValueError("Invalid scope")
    destination.parent.mkdir(parents=True,exist_ok=True)
    if not destination.exists(): shutil.copy2(source,destination)
    with connect() as db: db.execute("UPDATE ingestion_items SET status='approved',review_reason=NULL,scope_id=?,staged_path=? WHERE id=?",(scope_id,str(destination.relative_to(ROOT)),item_id))
    return str(destination)

def classify(path: Path):
    n=path.name.lower(); full=str(path).lower()
    typ="chatgpt" if "chatgpt" in full or n=="conversations.json" else "claude" if "claude" in full else "savvy" if "savvy" in full else "candidate"
    safe=typ in {"chatgpt","claude","savvy"} and path.suffix.lower() in TEXT and path.stat().st_size <= 20_000_000
    return typ, safe

def audit(roots: list[Path], stage: bool=True) -> dict:
    result={"staged":0,"review":0,"duplicate":0}; dest=ROOT/"data"/"ingestion"/"staged"; dest.mkdir(parents=True,exist_ok=True)
    for root in roots:
      if not root.exists(): continue
      for p in root.rglob("*"):
        try:
          if not p.is_file() or p.stat().st_size>100_000_000 or any(x in p.parts for x in (".git","node_modules","Library")): continue
          typ,safe=classify(p)
          if not safe and not any(k in p.name.lower() for k in ("agent","project","memory","export")): continue
          digest=hashlib.sha256(p.read_bytes()).hexdigest(); existing=None
          with connect() as db: existing=db.execute("SELECT id FROM ingestion_items WHERE sha256=?",(digest,)).fetchone()
          status="duplicate" if existing else "staged" if safe and stage else "review"
          staged=None
          if status=="staged":
            target=dest/f"{digest[:12]}-{p.name}"; shutil.copy2(p,target); staged=str(target.relative_to(ROOT)); result["staged"]+=1
          else: result[status]+=1
          with connect() as db: db.execute("INSERT INTO ingestion_items(source_path,source_type,sha256,size,modified,scope_id,status,review_reason,staged_path,discovered_at) VALUES(?,?,?,?,?,'master',?,?,?,?) ON CONFLICT(source_path) DO UPDATE SET sha256=excluded.sha256,size=excluded.size,modified=excluded.modified,status=excluded.status,review_reason=excluded.review_reason,staged_path=excluded.staged_path",(str(p),typ,digest,p.stat().st_size,p.stat().st_mtime,status,None if safe else "Ambiguous candidate; approval required",staged,now()))
        except (OSError,PermissionError): continue
    return result
