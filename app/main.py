from pathlib import Path
import os
from fastapi import FastAPI,HTTPException
from .core.models import TaskRequest
from .orchestrator import Orchestrator
ROOT=Path(os.environ.get("PROMETHEUS_WORKSPACE",Path.cwd())).resolve();DATA=Path(os.environ.get("PROMETHEUS_DATA",ROOT/".prometheus"));agent=Orchestrator(ROOT,DATA)
app=FastAPI(title="Prometheus",version="0.1.0")
@app.get("/health")
def health():return {"status":"ok","agent":"prometheus","workspace":str(ROOT)}
@app.post("/tasks")
def create_task(request:TaskRequest):
    if not request.goal.strip():raise HTTPException(400,"goal required")
    return agent.run(request).model_dump()
@app.get("/memory")
def memory(q:str=""):return {"items":agent.memory.search(q)}
