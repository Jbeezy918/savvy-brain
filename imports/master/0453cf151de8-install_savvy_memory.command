#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$HOME/SavvyMemory"
VENV="$ROOT/.venv"
PYTHON="${PYTHON:-python3}"

echo "==> Installing Savvy Memory at $ROOT"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "ERROR: python3 is required. Install Python 3.10+ and rerun."
  exit 1
fi

"$PYTHON" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("ERROR: Python 3.10+ is required.")
print("Python:", sys.version.split()[0])
PY

mkdir -p \
  "$ROOT/knowledge" \
  "$ROOT/projects/H-Mountain" \
  "$ROOT/clients" \
  "$ROOT/business" \
  "$ROOT/index" \
  "$ROOT/logs"

"$PYTHON" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip wheel
"$VENV/bin/pip" install \
  "mcp[cli]>=1.0,<2" \
  "chromadb>=1.0,<2" \
  "sentence-transformers>=5,<6" \
  "pypdf>=5,<7" \
  "python-docx>=1.1,<2"

cat <<'PY' > "$ROOT/server.py"
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Iterable

import chromadb
from docx import Document
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

ROOT = Path(os.environ.get("SAVVY_MEMORY_ROOT", Path.home() / "SavvyMemory")).expanduser().resolve()
INDEX = ROOT / "index"
COLLECTION_NAME = "savvy_memory"
MODEL_NAME = os.environ.get(
    "SAVVY_EMBED_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

TEXT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".rst", ".csv", ".tsv", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml", ".html",
    ".htm", ".css", ".scss", ".js", ".jsx", ".ts", ".tsx", ".py", ".sh",
    ".sql", ".java", ".go", ".rs", ".php", ".rb", ".c", ".h", ".cpp",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic"}

mcp = FastMCP("Savvy Memory", json_response=True)
_client = chromadb.PersistentClient(path=str(INDEX))
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)
_model: SentenceTransformer | None = None


def model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def safe_path(relative_path: str = "") -> Path:
    candidate = (ROOT / relative_path).expanduser().resolve()
    if candidate != ROOT and ROOT not in candidate.parents:
        raise ValueError("Path must remain inside ~/SavvyMemory")
    return candidate


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        return path.read_text(encoding="utf-8", errors="replace")

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n\n".join((page.extract_text() or "") for page in reader.pages)

    if suffix == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)

    if suffix in IMAGE_EXTENSIONS:
        sidecar = path.with_suffix(path.suffix + ".md")
        if sidecar.exists():
            return (
                f"IMAGE ASSET: {path.name}\n"
                f"PATH: {path.relative_to(ROOT)}\n\n"
                f"{sidecar.read_text(encoding='utf-8', errors='replace')}"
            )
        return (
            f"IMAGE ASSET: {path.name}\n"
            f"PATH: {path.relative_to(ROOT)}\n"
            "No textual description exists. Create a sidecar file named "
            f"{path.name}.md describing the image, customer feedback, and intended use."
        )

    return ""


def chunk_text(text: str, size: int = 1400, overlap: int = 220) -> list[str]:
    clean = re.sub(r"\r\n?", "\n", text).strip()
    if not clean:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n{2,}", clean) if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 <= size:
            current = f"{current}\n\n{paragraph}".strip()
            continue

        if current:
            chunks.append(current)

        if len(paragraph) <= size:
            current = paragraph
            continue

        start = 0
        while start < len(paragraph):
            end = min(start + size, len(paragraph))
            chunks.append(paragraph[start:end])
            if end == len(paragraph):
                break
            start = max(end - overlap, start + 1)
        current = ""

    if current:
        chunks.append(current)

    return chunks


def eligible_files(base: Path) -> Iterable[Path]:
    excluded = {".venv", "index", ".git", "__pycache__", "logs"}
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if any(part in excluded for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS | {".pdf", ".docx"} | IMAGE_EXTENSIONS:
            yield path


def file_signature(path: Path) -> str:
    stat = path.stat()
    raw = f"{path.relative_to(ROOT)}:{stat.st_mtime_ns}:{stat.st_size}"
    return hashlib.sha256(raw.encode()).hexdigest()


def index_paths(paths: list[Path]) -> dict:
    documents: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []
    files_indexed = 0
    skipped = []

    for path in paths:
        try:
            text = extract_text(path)
            chunks = chunk_text(text)
            if not chunks:
                skipped.append(str(path.relative_to(ROOT)))
                continue

            rel = str(path.relative_to(ROOT))
            sig = file_signature(path)

            existing = _collection.get(where={"path": rel}, include=[])
            if existing.get("ids"):
                _collection.delete(ids=existing["ids"])

            for number, chunk in enumerate(chunks):
                ids.append(hashlib.sha256(f"{sig}:{number}".encode()).hexdigest())
                documents.append(chunk)
                metadatas.append(
                    {
                        "path": rel,
                        "filename": path.name,
                        "extension": path.suffix.lower(),
                        "chunk": number,
                        "signature": sig,
                    }
                )
            files_indexed += 1
        except Exception as exc:
            skipped.append(f"{path.relative_to(ROOT)}: {exc}")

    if documents:
        embeddings = model().encode_document(
            documents,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()
        batch = 256
        for start in range(0, len(documents), batch):
            end = start + batch
            _collection.upsert(
                ids=ids[start:end],
                documents=documents[start:end],
                metadatas=metadatas[start:end],
                embeddings=embeddings[start:end],
            )

    return {
        "root": str(ROOT),
        "files_indexed": files_indexed,
        "chunks_written": len(documents),
        "skipped": skipped[:50],
        "collection_count": _collection.count(),
    }


@mcp.tool()
def index_memory(relative_path: str = "") -> dict:
    """Index or refresh documents inside ~/SavvyMemory. Use a relative folder such as projects/H-Mountain."""
    base = safe_path(relative_path)
    if not base.exists():
        raise ValueError(f"Path does not exist: {base}")
    paths = [base] if base.is_file() else list(eligible_files(base))
    return index_paths(paths)


@mcp.tool()
def search_memory(query: str, project: str = "", limit: int = 8) -> dict:
    """Semantic search across local personal and project memory. Optionally filter by project-folder text."""
    limit = max(1, min(limit, 20))
    if _collection.count() == 0:
        return {"results": [], "message": "Index is empty. Run index_memory first."}

    query_embedding = model().encode_query(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    ).tolist()

    where = {"path": {"$contains": project}} if project else None
    result = _collection.query(
        query_embeddings=query_embedding,
        n_results=limit,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    rows = []
    for document, metadata, distance in zip(
        result.get("documents", [[]])[0],
        result.get("metadatas", [[]])[0],
        result.get("distances", [[]])[0],
    ):
        rows.append(
            {
                "path": metadata["path"],
                "chunk": metadata["chunk"],
                "relevance": round(1.0 - float(distance), 4),
                "text": document,
            }
        )

    return {"query": query, "project_filter": project, "results": rows}


@mcp.tool()
def read_memory_file(relative_path: str, max_chars: int = 12000) -> dict:
    """Read one text, PDF, DOCX, or image-description file from ~/SavvyMemory."""
    path = safe_path(relative_path)
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    max_chars = max(500, min(max_chars, 50000))
    text = extract_text(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "content": text[:max_chars],
        "truncated": len(text) > max_chars,
        "total_characters": len(text),
    }


@mcp.tool()
def list_memory_files(relative_path: str = "", limit: int = 200) -> dict:
    """List local memory files without loading their contents."""
    base = safe_path(relative_path)
    if not base.exists():
        raise ValueError(f"Path does not exist: {base}")
    limit = max(1, min(limit, 1000))
    files = []
    paths = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file())
    for path in paths:
        if any(part in {".venv", "index", ".git", "__pycache__"} for part in path.relative_to(ROOT).parts):
            continue
        files.append(
            {
                "path": str(path.relative_to(ROOT)),
                "size_bytes": path.stat().st_size,
                "extension": path.suffix.lower(),
            }
        )
        if len(files) >= limit:
            break
    return {"root": str(ROOT), "files": files}


@mcp.tool()
def memory_status() -> dict:
    """Show local memory location, indexed chunk count, and embedding model."""
    return {
        "root": str(ROOT),
        "index": str(INDEX),
        "collection": COLLECTION_NAME,
        "indexed_chunks": _collection.count(),
        "embedding_model": MODEL_NAME,
        "storage": "local",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
PY

cat <<'PY' > "$ROOT/index_now.py"
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from server import ROOT, eligible_files, index_paths  # noqa: E402

result = index_paths(list(eligible_files(ROOT)))
print(__import__("json").dumps(result, indent=2))
PY

cat <<'SH' > "$ROOT/savvy-memory"
#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$HOME/SavvyMemory"
case "${1:-}" in
  index)
    exec "$ROOT/.venv/bin/python" "$ROOT/index_now.py"
    ;;
  serve)
    exec "$ROOT/.venv/bin/python" "$ROOT/server.py"
    ;;
  open)
    open "$ROOT"
    ;;
  *)
    echo "Usage: $0 {index|serve|open}"
    exit 1
    ;;
esac
SH
chmod +x "$ROOT/savvy-memory"

cat <<'MD' > "$ROOT/projects/H-Mountain/README.md"
# H Mountain Project Memory

Place concise project documentation here:

- CUSTOMER_REQUIREMENTS.md
- BRAND_GUIDE.md
- PROJECT_STATE.md
- ARCHITECTURE.md
- CURRENT_TASK.md
- ROADMAP.md
- KNOWN_ISSUES.md
- API_INDEX.md
- DESIGN_DECISIONS.md
- CHANGELOG.md

Place original assets in an `assets/` subfolder.

For each important image, create a sidecar description using the exact image filename plus `.md`.

Example:

`property-map.png`
`property-map.png.md`

The sidecar should describe what the image contains, the client's feedback, approved usage, and any design constraints.
MD

cat <<'MD' > "$ROOT/README.md"
# Savvy Memory

Local RAG memory exposed through MCP.

## Folders

- `projects/` — project-specific knowledge
- `clients/` — client requirements and decisions
- `business/` — reusable business knowledge
- `knowledge/` — general SOPs and reference material
- `index/` — local Chroma vector database

## Commands

- `~/SavvyMemory/savvy-memory index`
- `~/SavvyMemory/savvy-memory serve`
- `~/SavvyMemory/savvy-memory open`

After adding or changing documents, rerun the index command.

## Suggested Claude instruction

Use Savvy Memory before loading large project folders. Search first, read only the most relevant files, and keep MCP output targeted. Never request the entire knowledge base at once.
MD

echo "==> Running initial local index. The embedding model downloads once on first run."
"$VENV/bin/python" "$ROOT/index_now.py"

if command -v claude >/dev/null 2>&1; then
  echo "==> Configuring Claude Code user-scoped MCP server"
  claude mcp remove savvy-memory --scope user >/dev/null 2>&1 || true
  claude mcp add --scope user --transport stdio savvy-memory -- \
    "$VENV/bin/python" "$ROOT/server.py"
  echo "==> Claude Code configuration:"
  claude mcp get savvy-memory || true
else
  cat <<EOF

Claude Code CLI was not found, so automatic MCP registration was skipped.

After installing Claude Code, run:

claude mcp add --scope user --transport stdio savvy-memory -- \
"$VENV/bin/python" "$ROOT/server.py"

EOF
fi

cat <<EOF

============================================================
SAVVY MEMORY INSTALLED
============================================================

Memory folder:
  $ROOT

H Mountain folder:
  $ROOT/projects/H-Mountain

Open it:
  open "$ROOT"

Re-index after adding files:
  "$ROOT/savvy-memory" index

Claude Code status:
  claude mcp get savvy-memory

First Claude request:
  "Use the savvy-memory MCP server. Call memory_status, then search_memory
   for the H Mountain requirements. Do not load every file."

IMPORTANT:
- Your source documents and vector database remain on this computer.
- The AI still receives the specific snippets returned by MCP when it calls a tool.
- Images are stored locally; add .md sidecars so they are semantically searchable.
============================================================
EOF
