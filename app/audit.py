from __future__ import annotations
import json,sqlite3
from pathlib import Path
from datetime import datetime,timezone
class AuditLog:
    def __init__(self,path:Path):
        self.path=path;path.parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(path) as db:db.execute("CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,event TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL)")
    def write(self,event,payload):
        with sqlite3.connect(self.path) as db:db.execute("INSERT INTO audit(event,payload,created_at) VALUES(?,?,?)",(event,json.dumps(payload),datetime.now(timezone.utc).isoformat()))
