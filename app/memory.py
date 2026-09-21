from __future__ import annotations
import json,sqlite3
from pathlib import Path
from datetime import datetime,timezone
class MemoryStore:
    def __init__(self,path:Path):
        self.path=path;path.parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(path) as db:db.execute("CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY,key TEXT,value TEXT,source TEXT,verified INTEGER,created_at TEXT)")
    def put(self,key,value,source,verified=False):
        with sqlite3.connect(self.path) as db:db.execute("INSERT INTO memories(key,value,source,verified,created_at) VALUES(?,?,?,?,?)",(key,json.dumps(value),source,int(verified),datetime.now(timezone.utc).isoformat()))
    def search(self,key,limit=20):
        with sqlite3.connect(self.path) as db:rows=db.execute("SELECT key,value,source,verified,created_at FROM memories WHERE key LIKE ? ORDER BY id DESC LIMIT ?",(f"%{key}%",limit)).fetchall()
        return [{"key":r[0],"value":json.loads(r[1]),"source":r[2],"verified":bool(r[3]),"created_at":r[4]} for r in rows]
