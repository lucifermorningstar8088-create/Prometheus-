from app.core.task import Task, TaskState
from app.policy import PolicyEngine, ToolPolicy
from app.tool_registry import Tool, ToolRegistry


def test_task_state_machine():
    task = Task("t1", "test")
    task.transition(TaskState.PLANNED)
    task.transition(TaskState.AUTHORIZED)
    task.transition(TaskState.RUNNING)
    task.transition(TaskState.VERIFYING)
    task.transition(TaskState.SUCCESS)
    assert task.state is TaskState.SUCCESS


def test_invalid_transition_rejected():
    task = Task("t1", "test")
    try:
        task.transition(TaskState.SUCCESS)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid transition accepted")


def test_policy_is_least_privilege():
    engine = PolicyEngine()
    engine.register(ToolPolicy("safe", "low", frozenset({"read"})))
    engine.authorize("safe", {"read"})

    try:
        engine.authorize("safe", set())
    except PermissionError:
        pass
    else:
        raise AssertionError("missing permission accepted")


def test_approval_gate():
    engine = PolicyEngine()
    engine.register(ToolPolicy("deploy", "high", frozenset({"deploy"}), approval_required=True))
    try:
        engine.authorize("deploy", {"deploy"})
    except PermissionError:
        pass
    else:
        raise AssertionError("approval bypassed")
    engine.authorize("deploy", {"deploy"}, approved=True)


def test_tool_registry():
    registry = ToolRegistry()
    registry.register(Tool("noop", lambda: None, "test tool"))
    assert registry.get("noop").name == "noop"
    assert registry.names() == ("noop",)
