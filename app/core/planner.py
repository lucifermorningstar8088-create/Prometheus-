from .models import PlanStep,Risk
class Planner:
    def plan(self,goal:str)->list[PlanStep]:
        g=goal.lower(); steps=[PlanStep(id="inspect",action="Inspect workspace",tool="workspace_inspect",acceptance=["inspection completed"])]
        if any(x in g for x in ("test","fix","debug","project","code","build")):
            steps += [PlanStep(id="test",action="Run discoverable project tests",tool="project_test",acceptance=["test result captured"]),PlanStep(id="verify",action="Verify evidence",tool="verify",acceptance=["verification recorded"])]
        else: steps.append(PlanStep(id="verify",action="Verify evidence",tool="verify",acceptance=["verification recorded"]))
        if any(x in g for x in ("deploy","publish","send","delete","payment","production")):
            for s in steps: s.requires_approval=True; s.risk=Risk.HIGH
        return steps
