# Handles memory, learning, logging.
import sqlite3, json, time, traceback, pathlib

DB = "memory.db"
LOG = "logs.jsonl"

def _db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS memory(ts REAL, kind TEXT, data TEXT)")
    return conn

def remember(kind, data):
    conn=_db()
    conn.execute("INSERT INTO memory VALUES(?,?,?)",(time.time(),kind,json.dumps(data)))
    conn.commit(); conn.close()
    with open(LOG,"a") as f: f.write(json.dumps({"ts":time.time(),"kind":kind,"data":data})+"\n")

def recall(limit=20):
    conn=_db()
    cur=conn.execute("SELECT ts,kind,data FROM memory ORDER BY ts DESC LIMIT ?",(limit,))
    out=[{"ts":ts,"kind":k,"data":json.loads(d)} for ts,k,d in cur.fetchall()]
    conn.close(); return out

def learn(error=None,success=None):
    if error: remember("error",{"trace":traceback.format_exc(),"msg":str(error)})
    if success: remember("success",success)