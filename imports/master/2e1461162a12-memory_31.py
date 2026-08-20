from __future__ import annotations
import sqlite3, time, os, contextlib
from pathlib import Path
import json, numpy as np

DB = os.getenv("AGENT_MEMORY_DB", "state/memory.db")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
Path("state").mkdir(exist_ok=True, parents=True)

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY, project TEXT, text TEXT, tags TEXT, source TEXT, ts REAL);
CREATE INDEX IF NOT EXISTS idx_facts ON facts(project, ts DESC);
CREATE TABLE IF NOT EXISTS docs(id INTEGER PRIMARY KEY, project TEXT, title TEXT, url TEXT, content TEXT, ts REAL);
CREATE INDEX IF NOT EXISTS idx_docs ON docs(project, ts DESC);
"""

class Memory:
    def __init__(self, path: str = DB):
        self.path = path
        Path(Path(path).parent).mkdir(parents=True, exist_ok=True)
        with self._conn() as con:
            for stmt in SCHEMA.strip().split(";\n"):
                s = stmt.strip()
                if s: con.execute(s)

    @contextlib.contextmanager
    def _conn(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        try: yield con; con.commit()
        finally: con.close()

    def add_fact(self, text: str, project="global", tags=None, source=""):
        with self._conn() as con:
            con.execute("INSERT INTO facts(project,text,tags,source,ts) VALUES(?,?,?,?,?)",
                        (project, text.strip(), ",".join(tags or []), source, time.time()))

    def find_facts(self, query: str, project="global", limit=20):
        q = f"%{query.lower()}%"
        with self._conn() as con:
            rows = con.execute("""SELECT project,text,tags,source,ts FROM facts
                                  WHERE project=? AND lower(text) LIKE ? ORDER BY ts DESC LIMIT ?""",
                               (project,q,limit)).fetchall()
        return [dict(r) for r in rows]

    def add_doc(self, title: str, content: str, project="global", url=""):
        with self._conn() as con:
            con.execute("INSERT INTO docs(project,title,url,content,ts) VALUES(?,?,?,?,?)",
                        (project, title[:200], url, content[:200000], time.time()))

    def latest(self, project="global", kf=80, kd=8):
        with self._conn() as con:
            facts = con.execute("SELECT text FROM facts WHERE project=? ORDER BY ts DESC LIMIT ?",(project,kf)).fetchall()
            docs  = con.execute("SELECT title,content FROM docs WHERE project=? ORDER BY ts DESC LIMIT ?",(project,kd)).fetchall()
        facts = [r["text"] for r in facts]
        docs  = [f"{r['title']}\n{(r['content'] or '')[:1200]}" for r in docs]
        return facts, docs

    def _embed(self, texts: list[str]) -> list[list[float]]|None:
        key = os.getenv("OPENAI_API_KEY")
        if not key or not texts: return None
        try:
            from openai import OpenAI
            cli = OpenAI()
            out = cli.embeddings.create(model=EMBED_MODEL, input=texts)
            return [d.embedding for d in out.data]
        except Exception:
            return None

    @staticmethod
    def _topk(query_vec, vecs, k):
        a = np.array(query_vec, dtype=np.float32)
        b = np.array(vecs, dtype=np.float32)
        a = a / (np.linalg.norm(a) + 1e-6)
        b = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-6)
        sims = (b @ a)
        idx = sims.argsort()[-k:][::-1]
        return idx, sims[idx]

    def semantic_context(self, question: str, project="global", k_facts=8, k_docs=2) -> str:
        facts, docs = self.latest(project, kf=80, kd=10)
        candidates = [("fact", t) for t in facts] + [("doc", t) for t in docs]
        texts = [t for _,t in candidates]
        E = self._embed([question] + texts)
        if E:
            qv, pool = E[0], E[1:]
            idx, _ = self._topk(qv, pool, min(len(pool), k_facts + k_docs))
            picked = [candidates[i] for i in idx]
            f = [t for k,t in picked if k=="fact"][:k_facts]
            d = [t for k,t in picked if k=="doc"][:k_docs]
        else:
            low = question.lower().split()
            def score(t): return sum(w in t.lower() for w in low)
            ranked = sorted(candidates, key=lambda x: score(x[1]), reverse=True)
            f = [t for k,t in ranked if k=="fact"][:k_facts]
            d = [t for k,t in ranked if k=="doc"][:k_docs]
        parts=[]
        if f: parts.append("FACTS:\n" + "\n".join(f"- {x}" for x in f))
        if d: parts.append("DOCS:\n"  + "\n\n".join("# " + x.splitlines()[0] + "\n" + "\n".join(x.splitlines()[1:])[:800] for x in d))
        return "\n\n".join(parts)
