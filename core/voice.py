"""Dictation transcription and macOS speech rendering."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

from core.storage import ROOT


def speak_now(text: str, voice: str = "Daniel", rate: int = 170):
    """Speak text immediately (non-blocking, for dashboard Play buttons)."""
    if not text or not text.strip():
        return
    cmd = ["say", "-v", voice, "-r", str(rate), text]
    thread = Thread(target=lambda: subprocess.run(cmd, timeout=60), daemon=True)
    thread.start()


def speak(text: str, voice: str = "Samantha") -> Path:
    speech_dir = ROOT / "data" / "speech"
    speech_dir.mkdir(parents=True, exist_ok=True)
    output = speech_dir / f"reply-{uuid.uuid4().hex}.aiff"
    subprocess.run(["say", "-v", voice, "-o", str(output), text], check=True, timeout=180)
    return output


def transcribe(audio_bytes: bytes, filename: str = "dictation.wav") -> str:
    key = os.environ.get("LLM_API_KEY")
    if not key:
        raise RuntimeError("Dictation transcription needs LLM_API_KEY. Typed chat still works without it.")
    boundary = f"----Savvy{uuid.uuid4().hex}"
    fields = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{os.getenv('TRANSCRIPTION_MODEL', 'whisper-1')}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\nContent-Type: audio/wav\r\n\r\n".encode() + audio_bytes + b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    base = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    request = Request(f"{base}/audio/transcriptions", data=b"".join(fields), headers={
        "Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"
    })
    with urlopen(request, timeout=300) as response:
        return json.load(response)["text"]

