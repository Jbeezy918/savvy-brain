"""Project context assembly and local/OpenAI-compatible LLM clients."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from core.storage import ROOT


def load_project(project: str) -> tuple[Path, dict, str]:
    folder = (ROOT / "ideas" / project).resolve()
    if folder.parent != (ROOT / "ideas").resolve() or not folder.is_dir():
        raise ValueError("Unknown project")
    config = json.loads((folder / "brain.json").read_text(encoding="utf-8"))
    pieces = []
    for name in ("README.md", "GOALS.md", "MEMORY.md", "PROMPT.md"):
        path = folder / name
        if path.exists():
            pieces.append(f"## {name}\n{path.read_text(encoding='utf-8')}")
    return folder, config, "\n\n".join(pieces)


def generate(provider: str, model: str, system: str, prompt: str) -> str:
    if provider == "ollama":
        payload = {"model": model, "system": system, "prompt": prompt, "stream": False}
        request = Request(
            os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate"),
            data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=600) as response:
            return json.load(response)["response"]
    if provider == "openai-compatible":
        base = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        key = os.environ["LLM_API_KEY"]
        payload = {"model": model, "messages": [
            {"role": "system", "content": system}, {"role": "user", "content": prompt}
        ]}
        request = Request(f"{base}/chat/completions", data=json.dumps(payload).encode(), headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {key}"
        })
        with urlopen(request, timeout=600) as response:
            return json.load(response)["choices"][0]["message"]["content"]
    raise ValueError(f"Unsupported provider: {provider}")

