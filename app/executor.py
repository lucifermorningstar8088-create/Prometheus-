from __future__ import annotations
import os,subprocess
from pathlib import Path
from .core.models import ToolResult
class Executor:
    def __init__(self,workspace:Path): self.workspace=workspace.resolve()
    def inspect(self)->ToolResult:
        items=[p.name for p in sorted(self.workspace.iterdir()) if p.name not in {".git",".venv","__pycache__"}]
        return ToolResult(ok=True,output="\\n".join(items) or "(empty workspace)",evidence={"workspace":str(self.workspace)})
    def project_test(self)->ToolResult:
        if (self.workspace/"pyproject.toml").exists(): cmd=[os.environ.get("PYTHON","python"),"-m","pytest","-q"]
        elif (self.workspace/"package.json").exists(): cmd=["npm","test"]
        else: return ToolResult(ok=True,output="No supported test command discovered.",evidence={"tested":False})
        try:
            p=subprocess.run(cmd,cwd=self.workspace,capture_output=True,text=True,timeout=120,shell=False)
            out=(p.stdout+"\\n"+p.stderr).strip()[-12000:]
            return ToolResult(ok=p.returncode==0,output=out,error=None if p.returncode==0 else f"exit_code={p.returncode}",evidence={"command":cmd,"exit_code":p.returncode})
        except Exception as e:return ToolResult(ok=False,error=str(e))
