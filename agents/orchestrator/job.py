"""
Job and Step data models for the Orchestrator.

A Job is the top-level unit of work requested by a user or external system.
A Job is composed of one or more Steps, each assigned to a specific agent role.

State machine:
  Job:   pending → running → completed | failed | cancelled
  Step:  pending → running → completed | failed | skipped
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Step:
    step_id: str = field(default_factory=lambda: uuid4().hex[:8])
    name: str = ""
    description: str = ""
    assigned_role: str = ""          # which agent role should handle this
    skill: str = ""                  # skill to invoke (optional)
    params: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)   # step_ids
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str = ""
    started_at: float | None = None
    finished_at: float | None = None
    attempts: int = 0
    max_attempts: int = 2

    def start(self) -> None:
        self.status = StepStatus.RUNNING
        self.started_at = time.time()
        self.attempts += 1

    def complete(self, result: Any) -> None:
        self.status = StepStatus.COMPLETED
        self.result = result
        self.finished_at = time.time()

    def fail(self, error: str) -> None:
        self.status = StepStatus.FAILED
        self.error = error
        self.finished_at = time.time()

    def can_retry(self) -> bool:
        return self.status == StepStatus.FAILED and self.attempts < self.max_attempts

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "description": self.description,
            "assigned_role": self.assigned_role,
            "skill": self.skill,
            "params": self.params,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Step":
        return cls(
            step_id=data.get("step_id", uuid4().hex[:8]),
            name=data.get("name", ""),
            description=data.get("description", ""),
            assigned_role=data.get("assigned_role", ""),
            skill=data.get("skill", ""),
            params=data.get("params") or {},
            depends_on=data.get("depends_on") or [],
            status=StepStatus(data.get("status", "pending")),
            result=data.get("result"),
            error=data.get("error", ""),
            started_at=data.get("started_at"),
            finished_at=data.get("finished_at"),
            attempts=data.get("attempts", 0),
            max_attempts=data.get("max_attempts", 2),
        )


@dataclass
class Job:
    job_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    requested_by: str = "user"
    steps: list[Step] = field(default_factory=list)
    status: JobStatus = JobStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    finished_at: float | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Step accessors
    # ------------------------------------------------------------------

    def add_step(self, step: Step) -> "Job":
        self.steps.append(step)
        return self

    def get_step(self, step_id: str) -> Step | None:
        return next((s for s in self.steps if s.step_id == step_id), None)

    def ready_steps(self) -> list[Step]:
        """Return steps whose dependencies are all completed and are still pending."""
        completed_ids = {s.step_id for s in self.steps if s.status == StepStatus.COMPLETED}
        return [
            s for s in self.steps
            if s.status == StepStatus.PENDING
            and all(dep in completed_ids for dep in s.depends_on)
        ]

    def retryable_steps(self) -> list[Step]:
        return [s for s in self.steps if s.can_retry()]

    def results_by_name(self) -> dict[str, Any]:
        """Return {step_name: result} for every completed step."""
        return {
            s.name: s.result
            for s in self.steps
            if s.status == StepStatus.COMPLETED
        }

    def is_done(self) -> bool:
        return all(
            s.status in (StepStatus.COMPLETED, StepStatus.FAILED, StepStatus.SKIPPED)
            for s in self.steps
        )

    def has_failures(self) -> bool:
        return any(s.status == StepStatus.FAILED for s in self.steps)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        self.status = JobStatus.RUNNING
        self.started_at = time.time()

    def complete(self) -> None:
        self.status = JobStatus.COMPLETED
        self.finished_at = time.time()

    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error
        self.finished_at = time.time()

    def cancel(self) -> None:
        self.status = JobStatus.CANCELLED
        self.finished_at = time.time()
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                step.status = StepStatus.SKIPPED

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "requested_by": self.requested_by,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "error": self.error,
            "steps": [s.to_dict() for s in self.steps],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Job":
        steps = [Step.from_dict(s) for s in data.get("steps", [])]
        return cls(
            job_id=data.get("job_id", str(uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            requested_by=data.get("requested_by", "user"),
            steps=steps,
            status=JobStatus(data.get("status", "pending")),
            created_at=data.get("created_at", time.time()),
            started_at=data.get("started_at"),
            finished_at=data.get("finished_at"),
            error=data.get("error", ""),
            metadata=data.get("metadata") or {},
        )
