from app.policy import PolicyEngine,ToolPolicy

def test_unknown_tool_denied():
 e=PolicyEngine()
 try:e.authorize("missing",set())
 except PermissionError:pass
 else:raise AssertionError("unknown tool was authorized")

def test_high_impact_requires_approval():
 e=PolicyEngine();e.register(ToolPolicy("deploy","high",frozenset({"deploy"}),approval_required=True))
 try:e.authorize("deploy",{"deploy"})
 except PermissionError:pass
 else:raise AssertionError("approval gate bypassed")
 e.authorize("deploy",{"deploy"},approved=True)
