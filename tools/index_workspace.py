"""Command-line workspace indexer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.indexer import index_workspace  # noqa: E402
from core.storage import initialize  # noqa: E402

initialize()
indexed, skipped = index_workspace()
print(f"Indexed {indexed} files; skipped {skipped}.")

