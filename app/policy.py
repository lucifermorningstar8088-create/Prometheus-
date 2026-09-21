from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ToolPolicy:
    name: str
    risk: str
    permissions: frozenset[str] = frozenset()
    approval_required: bool = False
    network: bool = False
    audit_required: bool = True
    allowed_paths: tuple[str, ...] = ()
    max_runtime_seconds: int = 60
    max_retries: int = 2


@dataclass(slots=True)
class PolicyEngine:
    tools: dict[str, ToolPolicy] = field(default_factory=dict)

    def register(self, policy: ToolPolicy) -> None:
        if policy.name in self.tools:
            raise ValueError(f"Tool already registered: {policy.name}")
        if policy.max_runtime_seconds <= 0 or policy.max_retries < 0:
            raise ValueError("Invalid resource limits")
        self.tools[policy.name] = policy

    def authorize(self, tool_name: str, granted: set[str], approved: bool = False) -> None:
        policy = self.tools.get(tool_name)
        if policy is None:
            raise PermissionError(f"Unknown tool: {tool_name}")
        if not policy.permissions.issubset(granted):
            raise PermissionError(f"Missing permissions for {tool_name}")
        if policy.approval_required and not approved:
            raise PermissionError(f"Explicit approval required for {tool_name}")
