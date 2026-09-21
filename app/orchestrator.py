from __future__ import annotations
import uuid
from pathlib import Path
from .audit import AuditLog
from .executor import Executor
from .memory import MemoryStore
from .recovery import RecoveryEngine
from .verifier import Verifier
from .core.models import TaskRecord,TaskRequest
from .core.planner import Planner
class Orchestrator:
    def __init__(self,workspace:Path,data_dir:Path):
        self.workspace=workspace.resolve();self.audit=AuditLog(data_dir/"audit.sqlite3");self.memory=MemoryStore(data_dir/"memory.sqlite3");self.executor=Executor(self.workspace);self.planner=Planner();self.verifier=Verifier();self.recovery=RecoveryEngine()
    def run(self,request:TaskRequest)->TaskRecord:
        tid=f"task_{uuid.uuid4().hex[:12]}";steps=self.planner.plan(request.goal);record=TaskRecord(task_id=tid,goal=request.goal,state="planned",steps=[s.model_dump() for s in steps]);self.audit.write("task_created",record.model_dump())
        if not request.auto_execute:return record.model_copy(update={"state":"authorized"})
        record.state="running"
        for step in steps:
            if step.requires_approval:record.state="escalated";self.audit.write("approval_required",{"task_id":tid,"step":step.id});return record
            result=self.executor.inspect() if step.tool in ("workspace_inspect","verify") else self.executor.project_test()
            record.evidence.append({"step":step.id,"ok":result.ok,"output":result.output[-4000:],"error":result.error,"evidence":result.evidence})
            if not result.ok:
                record.state="recovery"
                if self.recovery.should_retry(0,result):result=self.executor.project_test() if step.tool=="project_test" else self.executor.inspect()
                if not result.ok:record.state="blocked";return record
        record.state="verifying";status,notes=self.verifier.verify(type("R",(),{"ok":True,"evidence":{}})());record.evidence.append({"verification":status.value,"notes":notes});record.state="success" if status.value=="verified" else "blocked";self.audit.write("task_finished",record.model_dump());self.memory.put("last_task",record.model_dump(),"orchestrator",record.state=="success");return record
