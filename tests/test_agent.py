from pathlib import Path
from app.orchestrator import Orchestrator
from app.core.models import TaskRequest
def test_plan_only(tmp_path:Path):
 r=Orchestrator(tmp_path,tmp_path/"data").run(TaskRequest(goal="inspect my project"));assert r.state=="authorized" and r.steps
def test_autonomous_inspection(tmp_path:Path):
 r=Orchestrator(tmp_path,tmp_path/"data").run(TaskRequest(goal="inspect my project",auto_execute=True));assert r.state=="success" and r.evidence
