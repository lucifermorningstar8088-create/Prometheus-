from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
class Risk(str, Enum):
    LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"
class VerificationStatus(str, Enum):
    VERIFIED="verified"; PARTIAL="partially_verified"; CONFLICTING="conflicting"; UNVERIFIED="unverified"; UNKNOWN="unknown"
class TaskRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=10000)
    auto_execute: bool = False
class TaskRecord(BaseModel):
    task_id: str; goal: str; state: str; risk: Risk=Risk.LOW
    steps: list[dict[str,Any]]=Field(default_factory=list); evidence: list[dict[str,Any]]=Field(default_factory=list)
    created_at: str=Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
class ToolResult(BaseModel):
    ok: bool; output: str=""; error: str|None=None; evidence: dict[str,Any]=Field(default_factory=dict)
class PlanStep(BaseModel):
    id: str; action: str; tool: str; risk: Risk=Risk.LOW; requires_approval: bool=False; acceptance: list[str]=Field(default_factory=list)
