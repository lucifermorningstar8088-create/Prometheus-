from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskState(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    AUTHORIZED = "authorized"
    RUNNING = "running"
    VERIFYING = "verifying"
    SUCCESS = "success"
    RECOVERY = "recovery"
    BLOCKED = "blocked"
    ESCALATED = "escalated"


@dataclass(slots=True)
class Task:
    task_id: str
    goal: str
    state: TaskState = TaskState.CREATED
    risk: str = "low"
    acceptance_criteria: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def transition(self, new_state: TaskState) -> None:
        allowed = {
            TaskState.CREATED: {TaskState.PLANNED, TaskState.BLOCKED},
            TaskState.PLANNED: {TaskState.AUTHORIZED, TaskState.BLOCKED, TaskState.ESCALATED},
            TaskState.AUTHORIZED: {TaskState.RUNNING, TaskState.BLOCKED},
            TaskState.RUNNING: {TaskState.VERIFYING, TaskState.RECOVERY, TaskState.BLOCKED, TaskState.ESCALATED},
            TaskState.VERIFYING: {TaskState.SUCCESS, TaskState.RECOVERY, TaskState.BLOCKED, TaskState.ESCALATED},
            TaskState.RECOVERY: {TaskState.RUNNING, TaskState.VERIFYING, TaskState.BLOCKED, TaskState.ESCALATED},
            TaskState.SUCCESS: set(),
            TaskState.BLOCKED: set(),
            TaskState.ESCALATED: set(),
        }
        if new_state not in allowed[self.state]:
            raise ValueError(f"Invalid transition: {self.state.value} -> {new_state.value}")
        self.state = new_state
