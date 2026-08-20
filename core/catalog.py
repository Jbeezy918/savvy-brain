"""Text extraction and deterministic first-pass knowledge profiling."""
from __future__ import annotations
import json,re,subprocess,zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree
from core.storage import ROOT,connect,now

PLAIN={".md",".txt",".py",".js",".json",".yaml",".yml",".csv",".toml",".html",".htm",".command"}
class _HTML(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):
  if data.strip():self.parts.append(data.strip())

def extract(path:Path,max_chars:int=2_000_000)->str:
 suffix=path.suffix.lower()
 if suffix in PLAIN:
  raw=path.read_text(encoding="utf-8",errors="replace")
  if suffix in {".html",".htm"}:p=_HTML();p.feed(raw);raw="\n".join(p.parts)
  return raw[:max_chars]
 if suffix==".docx":
  with zipfile.ZipFile(path) as z: root=ElementTree.fromstring(z.read("word/document.xml"))
  return "\n".join("".join(n.text or "" for n in p.iter()) for p in root.iter() if p.tag.endswith("}p"))[:max_chars]
 if suffix==".xlsx":
  with zipfile.ZipFile(path) as z:
   names=[n for n in z.namelist() if n.endswith("sharedStrings.xml")]
   if not names:return ""
   root=ElementTree.fromstring(z.read(names[0]));return "\n".join("".join(n.text or "" for n in x.iter()) for x in root)[:max_chars]
 if suffix==".pdf":
  try:return subprocess.run(["pdftotext",str(path),"-"],capture_output=True,text=True,timeout=90,check=True).stdout[:max_chars]
  except Exception:return ""
 return ""

def catalog_approved()->dict:
 counts={"cataloged":0,"no_text":0,"preferences":0,"ideas":0}
 with connect() as db: items=db.execute("SELECT * FROM ingestion_items WHERE status='approved'").fetchall()
 for item in items:
  path=ROOT/item["staged_path"]
  try:content=extract(path)
  except Exception:content=""
  if not content.strip():counts["no_text"]+=1;continue
  rel=str(path.relative_to(ROOT));project=item["scope_id"].split(":",1)[1] if item["scope_id"].startswith("project:") else None
  with connect() as db:
   db.execute("INSERT INTO documents(path,project,modified,size,content,indexed_at,scope_id) VALUES(?,?,?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET content=excluded.content,indexed_at=excluded.indexed_at,scope_id=excluded.scope_id",(rel,project,path.stat().st_mtime,path.stat().st_size,content,now(),item["scope_id"]))
  counts["cataloged"]+=1
  sentences=re.split(r"(?<=[.!?])\s+|[\r\n]+",content)
  for sentence in sentences:
   clean=" ".join(sentence.split())[:600]
   if not 20<=len(clean)<=600:continue
   lower=clean.lower();kind=None
   if any(x in lower for x in ("i like ","i love ","i prefer ","i want ","i don't like ","i do not like ")):kind="preference"
   elif any(x in lower for x in ("business idea","product idea","project idea","could build","opportunity","take off","market need")):kind="idea"
   if kind:
    with connect() as db:db.execute("INSERT OR IGNORE INTO knowledge_profiles(scope_id,profile_type,statement,source_path,confidence,created_at) VALUES(?,?,?,?,?,?)",(item["scope_id"],kind,clean,rel,.65,now()))
    counts[kind+"s"]+=1
 return counts
