#!/usr/bin/env python3
"""
GovConBrain Memory & RAG Library
=================================
Two memory systems for GovConPro agents:

1. VectorSearch  — ChromaDB-backed semantic search over the training corpus
                   (FAR rules, SBA regs, GSA guides, past opportunities)
                   Agents query this to "look things up" at runtime.

2. AgentMemory   — SQLite-backed personal memory
                   Agents store facts, lessons learned, vendor notes,
                   bid outcomes. Persists across sessions.

3. AgentBrain    — Combines both. Always loads AGENT_INSTRUCTIONS.md first.
                   This is what agents import and use.

Usage:
    from govconbrain_memory import AgentBrain
    brain = AgentBrain(agent_name="bid_researcher")
    brain.boot()                                    # loads instructions + primes context
    results = brain.search("SBA set-aside rules for small business")
    brain.remember("vendor", "R&S USA", "1-888-837-8772 — CMA180 federal pricing")
    brain.log("quoted", "W911SA26QA205", "Sent $82,400 quote to Dustin Robertson")
"""

import sqlite3, json, time, os, re
from pathlib import Path
from datetime import datetime
from typing import Optional

VAULT        = Path.home() / "GovConBrain"
VECTOR_DIR   = VAULT / "vector_db"
MEMORY_DB    = Path.home() / ".govcon_vault" / "agent_memory.db"
INSTRUCTIONS = VAULT / "memory" / "AGENT_INSTRUCTIONS.md"

# ──────────────────────────────────────────────────────────────────────────────
# VECTOR SEARCH  (ChromaDB)
# ──────────────────────────────────────────────────────────────────────────────

class VectorSearch:
    """Semantic search over the GovConBrain training corpus."""

    def __init__(self):
        self._client = None
        self._collection = None

    def _init(self):
        if self._client is not None:
            return
        try:
            import chromadb
            from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
            VECTOR_DIR.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(VECTOR_DIR))
            self._collection = self._client.get_or_create_collection(
                name="govconbrain",
                embedding_function=DefaultEmbeddingFunction(),
                metadata={"hnsw:space": "cosine"}
            )
        except ImportError:
            raise RuntimeError("ChromaDB not installed. Run: pip install chromadb --break-system-packages")

    def index_document(self, doc_id: str, text: str, metadata: dict):
        """Add or update a document in the vector index."""
        self._init()
        # ChromaDB max ~8000 chars per doc — chunk if needed
        chunks = [text[i:i+6000] for i in range(0, min(len(text), 24000), 6000)]
        for i, chunk in enumerate(chunks):
            cid = f"{doc_id}_chunk{i}" if len(chunks) > 1 else doc_id
            self._collection.upsert(
                ids=[cid],
                documents=[chunk],
                metadatas=[{**metadata, "chunk": i}]
            )

    def search(self, query: str, n_results: int = 5, category: str = None) -> list[dict]:
        """Semantic search. Returns list of {text, source, category, score}."""
        self._init()
        where = {"category": category} if category else None
        try:
            res = self._collection.query(
                query_texts=[query],
                n_results=min(n_results, self._collection.count() or 1),
                where=where,
                include=["documents", "metadatas", "distances"]
            )
        except Exception as e:
            return [{"text": f"Search error: {e}", "source": "", "category": "", "score": 0}]
        results = []
        for doc, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        ):
            results.append({
                "text":     doc,
                "source":   meta.get("source", ""),
                "category": meta.get("category", ""),
                "title":    meta.get("title", ""),
                "score":    round(1 - dist, 3)   # cosine → similarity
            })
        return results

    def count(self) -> int:
        self._init()
        return self._collection.count()

    def index_file(self, fpath: Path, category: str):
        """Index a single training .txt file."""
        self._init()
        text = fpath.read_text(errors="ignore")
        # Parse header fields written by processor
        source = ""
        title  = fpath.stem
        for line in text.splitlines()[:5]:
            if line.startswith("SOURCE:"):  source = line[7:].strip()
            if line.startswith("TITLE:"):   title  = line[6:].strip()
        body = text.split("="*10)[1].strip() if "="*10 in text else text
        doc_id = fpath.stem
        self.index_document(doc_id, body, {
            "source": source, "title": title,
            "category": category, "file": fpath.name
        })

    def index_all(self, training_dir: Path, verbose=True) -> int:
        """Index all .txt files in training subdirs. Returns count added."""
        self._init()
        total = 0
        for subdir in sorted(training_dir.iterdir()):
            if not subdir.is_dir(): continue
            category = subdir.name
            for fpath in subdir.glob("*.txt"):
                doc_id = fpath.stem
                # Skip if already indexed (check by id)
                existing = self._collection.get(ids=[doc_id])
                if existing["ids"]:
                    continue
                try:
                    self.index_file(fpath, category)
                    total += 1
                    if verbose:
                        print(f"  [IDX] {category}/{fpath.name[:50]}")
                except Exception as e:
                    if verbose:
                        print(f"  [ERR] {fpath.name}: {e}")
        return total


# ──────────────────────────────────────────────────────────────────────────────
# AGENT MEMORY  (SQLite)
# ──────────────────────────────────────────────────────────────────────────────

class AgentMemory:
    """
    Persistent memory for a named agent.
    Three tables:
      facts     — key/value knowledge (vendor phone, NAICS codes, preferences)
      episodes  — event log (bid submitted, email sent, quote received)
      lessons   — distilled takeaways ("always call POC before submitting")
    """

    def __init__(self, agent_name: str = "default"):
        self.agent_name = agent_name
        MEMORY_DB.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(MEMORY_DB), check_same_thread=False)
        self._setup()

    def _setup(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS facts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent       TEXT NOT NULL,
                category    TEXT NOT NULL,
                key         TEXT NOT NULL,
                value       TEXT NOT NULL,
                created_at  REAL,
                updated_at  REAL,
                importance  INTEGER DEFAULT 5,
                UNIQUE(agent, category, key)
            );
            CREATE TABLE IF NOT EXISTS episodes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent       TEXT NOT NULL,
                action      TEXT NOT NULL,
                detail      TEXT,
                contract_id TEXT,
                outcome     TEXT,
                ts          REAL
            );
            CREATE TABLE IF NOT EXISTS lessons (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                agent       TEXT NOT NULL,
                lesson      TEXT NOT NULL,
                context     TEXT,
                confidence  INTEGER DEFAULT 5,
                ts          REAL
            );
        """)
        self._conn.commit()

    # ── Facts ──────────────────────────────────────────────────────────────────

    def remember(self, key: str, value: str, category: str = "general", importance: int = 5):
        """Store or update a fact."""
        now = time.time()
        self._conn.execute("""
            INSERT INTO facts (agent, category, key, value, created_at, updated_at, importance)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(agent, category, key) DO UPDATE SET
                value=excluded.value, updated_at=excluded.updated_at,
                importance=excluded.importance
        """, (self.agent_name, category, key, value, now, now, importance))
        self._conn.commit()

    def recall(self, key: str, category: str = None) -> Optional[str]:
        """Retrieve a specific fact by key."""
        if category:
            row = self._conn.execute(
                "SELECT value FROM facts WHERE agent=? AND category=? AND key=?",
                (self.agent_name, category, key)
            ).fetchone()
        else:
            row = self._conn.execute(
                "SELECT value FROM facts WHERE agent=? AND key=? ORDER BY updated_at DESC LIMIT 1",
                (self.agent_name, key)
            ).fetchone()
        return row[0] if row else None

    def recall_category(self, category: str) -> dict:
        """Get all facts in a category."""
        rows = self._conn.execute(
            "SELECT key, value FROM facts WHERE agent=? AND category=? ORDER BY importance DESC",
            (self.agent_name, category)
        ).fetchall()
        return {k: v for k, v in rows}

    def recall_all(self) -> dict:
        """Get all facts grouped by category."""
        rows = self._conn.execute(
            "SELECT category, key, value FROM facts WHERE agent=? ORDER BY category, importance DESC",
            (self.agent_name,)
        ).fetchall()
        result = {}
        for cat, k, v in rows:
            result.setdefault(cat, {})[k] = v
        return result

    # ── Episodes ───────────────────────────────────────────────────────────────

    def log(self, action: str, detail: str = "", contract_id: str = "", outcome: str = ""):
        """Log an event/action taken."""
        self._conn.execute(
            "INSERT INTO episodes (agent, action, detail, contract_id, outcome, ts) VALUES (?,?,?,?,?,?)",
            (self.agent_name, action, detail, contract_id, outcome, time.time())
        )
        self._conn.commit()

    def recent_episodes(self, n: int = 20) -> list[dict]:
        """Get the N most recent episodes."""
        rows = self._conn.execute(
            "SELECT action, detail, contract_id, outcome, ts FROM episodes WHERE agent=? ORDER BY ts DESC LIMIT ?",
            (self.agent_name, n)
        ).fetchall()
        return [
            {"action": a, "detail": d, "contract": c, "outcome": o,
             "when": datetime.fromtimestamp(ts).strftime("%m/%d %H:%M")}
            for a, d, c, o, ts in rows
        ]

    # ── Lessons ────────────────────────────────────────────────────────────────

    def learn(self, lesson: str, context: str = "", confidence: int = 7):
        """Store a distilled lesson learned."""
        self._conn.execute(
            "INSERT INTO lessons (agent, lesson, context, confidence, ts) VALUES (?,?,?,?,?)",
            (self.agent_name, lesson, context, confidence, time.time())
        )
        self._conn.commit()

    def lessons(self, min_confidence: int = 5) -> list[str]:
        """Get all lessons above confidence threshold."""
        rows = self._conn.execute(
            "SELECT lesson FROM lessons WHERE agent=? AND confidence>=? ORDER BY confidence DESC, ts DESC",
            (self.agent_name, min_confidence)
        ).fetchall()
        return [r[0] for r in rows]

    def summary(self) -> str:
        """Human-readable memory summary for injecting into agent context."""
        lines = [f"=== {self.agent_name} Memory ==="]
        facts = self.recall_all()
        if facts:
            lines.append("\n-- Known Facts --")
            for cat, kv in facts.items():
                lines.append(f"[{cat}]")
                for k, v in kv.items():
                    lines.append(f"  {k}: {v}")
        ls = self.lessons()
        if ls:
            lines.append("\n-- Lessons Learned --")
            for l in ls[:10]:
                lines.append(f"  * {l}")
        eps = self.recent_episodes(5)
        if eps:
            lines.append("\n-- Recent Activity --")
            for e in eps:
                lines.append(f"  [{e['when']}] {e['action']}: {e['detail'][:80]}")
        return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# AGENT BRAIN  (combines both + instructions)
# ──────────────────────────────────────────────────────────────────────────────

class AgentBrain:
    """
    The full cognitive stack for a GovConPro agent.
    Always call brain.boot() at the start of any session.

    Example:
        brain = AgentBrain("bid_researcher")
        context = brain.boot()          # returns full context string to prime the agent
        hits = brain.search("FAR 13 simplified acquisition threshold")
        brain.remember("vendor", "TestEquity", "R&S authorized distributor, fast ship")
        brain.log("quoted", "Sent $82,400 to Robertson", contract_id="W911SA26QA205")
        brain.learn("Call POC before submitting — they often have unofficial guidance")
    """

    def __init__(self, agent_name: str = "govconpro_agent"):
        self.agent_name = agent_name
        self.memory  = AgentMemory(agent_name)
        self.vectors = VectorSearch()

    def boot(self) -> str:
        """
        Load everything the agent needs to start a session.
        Returns a context string suitable for injection into an LLM prompt.
        """
        sections = []

        # 1. Always read instructions first
        if INSTRUCTIONS.exists():
            sections.append("=== AGENT INSTRUCTIONS ===")
            sections.append(INSTRUCTIONS.read_text())
        else:
            sections.append("[WARNING] AGENT_INSTRUCTIONS.md not found — agent running without base instructions]")

        # 2. Personal memory
        mem_summary = self.memory.summary()
        if mem_summary:
            sections.append(mem_summary)

        # 3. Index stats
        try:
            count = self.vectors.count()
            sections.append(f"\n=== Knowledge Base: {count} indexed documents available via search() ===")
        except Exception:
            sections.append("\n=== Knowledge Base: vector index not yet built — run process_govconbrain.py ===")

        return "\n\n".join(sections)

    def search(self, query: str, n: int = 5, category: str = None) -> list[dict]:
        """Semantic search over the training corpus."""
        return self.vectors.search(query, n_results=n, category=category)

    def search_text(self, query: str, n: int = 3, category: str = None) -> str:
        """Search and return formatted text for prompt injection."""
        hits = self.search(query, n=n, category=category)
        if not hits:
            return f"[No results for: {query}]"
        lines = [f"--- Search: '{query}' ---"]
        for i, h in enumerate(hits, 1):
            lines.append(f"[{i}] ({h['category']}) {h['title']}\n{h['text'][:800]}\nSource: {h['source']}")
        return "\n\n".join(lines)

    # Convenience pass-throughs
    def remember(self, category: str, key: str, value: str, importance: int = 5):
        self.memory.remember(key, value, category=category, importance=importance)

    def recall(self, key: str, category: str = None) -> Optional[str]:
        return self.memory.recall(key, category=category)

    def log(self, action: str, detail: str = "", contract_id: str = "", outcome: str = ""):
        self.memory.log(action, detail, contract_id=contract_id, outcome=outcome)

    def learn(self, lesson: str, context: str = "", confidence: int = 7):
        self.memory.learn(lesson, context=context, confidence=confidence)


# ──────────────────────────────────────────────────────────────────────────────
# CLI — quick test / memory dump
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--search",  help="Test semantic search query")
    p.add_argument("--agent",   default="govconpro_agent")
    p.add_argument("--memory",  action="store_true", help="Dump agent memory")
    p.add_argument("--boot",    action="store_true", help="Show full boot context")
    p.add_argument("--index",   action="store_true", help="Index all training docs now")
    args = p.parse_args()

    brain = AgentBrain(args.agent)

    if args.index:
        print("Indexing all training docs...")
        n = brain.vectors.index_all(VAULT / "training", verbose=True)
        print(f"Done. +{n} new docs indexed. Total: {brain.vectors.count()}")
    elif args.search:
        hits = brain.search(args.search, n=5)
        for h in hits:
            print(f"\n[{h['score']:.2f}] ({h['category']}) {h['title']}")
            print(h["text"][:400])
    elif args.memory:
        print(brain.memory.summary())
    elif args.boot:
        print(brain.boot())
    else:
        p.print_help()
