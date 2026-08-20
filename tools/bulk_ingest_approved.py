#!/usr/bin/env python3
"""Bulk import explicitly approved personal/product data with hard safety exclusions."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core.catalog import catalog_approved
from core.ingestion import decide
from core.storage import initialize,rows

BLOCK=("/.venv/","/node_modules/","/__pycache__/","/.git/",".pyc",".env","secret","credential","private_key","private-key","api_key","apikey","access_token","wallet","keystore")
MAX=80_000_000

def scope_for(path:str)->str:
 low=path.lower()
 projects=[p.name for p in (ROOT/"ideas").iterdir() if p.is_dir()]
 for project in projects:
  if project.lower().replace("_"," ") in low.replace("_"," "):return f"project:{project}"
 return "master"

def run():
 initialize();result={"approved":0,"ignored_noise":0,"held_security":0,"errors":0}
 for item in rows("SELECT * FROM ingestion_items WHERE status='review' ORDER BY id"):
  low=item["source_path"].lower()
  try:
   if any(x in low for x in BLOCK):
    action="hold" if any(x in low for x in (".env","secret","credential","private_key","private-key","api_key","apikey","access_token","wallet","keystore")) else "ignore"
    decide(item["id"],action,"master");result["held_security" if action=="hold" else "ignored_noise"]+=1
   elif item["size"]>MAX:decide(item["id"],"hold","master");result["held_security"]+=1
   else:decide(item["id"],"approve",scope_for(item["source_path"]));result["approved"]+=1
  except Exception:result["errors"]+=1
 result["catalog"]=catalog_approved();return result

if __name__=="__main__":print(run())
