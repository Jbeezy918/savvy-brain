"""Truthful connector registry: configured means usable; available means adapter exists."""
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_project_env() -> None:
    """Load simple KEY=VALUE settings without overwriting the launch environment."""
    path = ROOT / ".env"
    if not path.exists(): return
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line=raw.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        key,value=line.split("=",1);key=key.strip();value=value.strip().strip('"').strip("'")
        if key and key.replace("_","").isalnum(): os.environ.setdefault(key,value)

load_project_env()

def registry():
    return [
      {"name":"Home Assistant","available":True,"configured":bool(os.getenv("HOME_ASSISTANT_URL") and os.getenv("HOME_ASSISTANT_TOKEN")),"needs":"HOME_ASSISTANT_URL + HOME_ASSISTANT_TOKEN"},
      {"name":"Browser research","available":True,"configured":False,"needs":"approved browser/research provider"},
      {"name":"Visualization / metrics","available":True,"configured":True,"needs":"none (local Streamlit charts)"},
      {"name":"Airtable sync","available":True,"configured":bool((os.getenv("AIRTABLE_TOKEN") or os.getenv("AIRTABLE_API_KEY")) and os.getenv("AIRTABLE_BASE_ID")),"needs":"AIRTABLE_TOKEN (PAT) + AIRTABLE_BASE_ID"},
      {"name":"Govee lighting","available":True,"configured":bool(os.getenv("GOVEE_API_KEY")),"needs":"GOVEE_API_KEY; read-only discovery before controls"},
      {"name":"LLM / dictation","available":True,"configured":bool(os.getenv("LLM_API_KEY")),"needs":"LLM_API_KEY; optional LLM_BASE_URL + TRANSCRIPTION_MODEL"},
    ]
