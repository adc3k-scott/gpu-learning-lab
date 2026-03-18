"""
Base classes for the Mission Control skill plugin system.

Every skill must:
  1. Inherit from BaseSkill
  2. Define class-level name, description, and optionally required_secrets
  3. Implement async execute(ctx, params) -> SkillResult
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class SkillContext:
    """
    Runtime context passed to every skill execution.

    Attributes:
        agent_id:      ID of the agent invoking the skill
        job_id:        ID of the job/task this execution belongs to
        state_store:   reference to the shared StateStore instance
        event_bus:     reference to the shared EventBus instance
        secrets:       dict of secret values the skill declared in required_secrets
        metadata:      arbitrary extra metadata set by the orchestrator
    """

    agent_id: str = ""
    job_id: str = ""
    state_store: Any = None
    event_bus: Any = None
    secrets: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillResult:
    """
    Standardised return type from skill.execute().

    Attributes:
        success:   True if the skill completed without error
        output:    Primary result value (any JSON-serialisable type)
        error:     Error message when success=False
        metadata:  Extra information (timing, token usage, etc.)
    """

    success: bool
    output: Any = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, output: Any = None, **meta) -> "SkillResult":
        return cls(success=True, output=output, metadata=meta)

    @classmethod
    def fail(cls, error: str, **meta) -> "SkillResult":
        return cls(success=False, error=error, metadata=meta)


@dataclass
class RetryPolicy:
    """
    Retry configuration for a skill.

    Attributes:
        max_attempts:  Total attempts before giving up (1 = no retry)
        backoff_base:  Base delay in seconds between attempts (exponential)
        exceptions:    Tuple of exception types that trigger a retry
    """

    max_attempts: int = 1
    backoff_base: float = 1.0
    exceptions: tuple[type[Exception], ...] = (Exception,)
    timeout: float = 300.0  # per-attempt timeout in seconds (0 = no timeout)


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class BaseSkill(ABC):
    """
    Abstract base class for all Mission Control skills.

    Class-level attributes (set on the subclass, not in __init__):
        name            str   — unique identifier, e.g. "file_manager"
        description     str   — human-readable one-liner
        version         str   — semver string, default "0.1.0"
        required_secrets list  — env-var names the skill needs in ctx.secrets
        retry_policy    RetryPolicy — auto-retry behaviour
    """

    name: str = ""
    description: str = ""
    version: str = "0.1.0"
    required_secrets: list[str] = []
    retry_policy: RetryPolicy = RetryPolicy()

    # ------------------------------------------------------------------
    # Contract
    # ------------------------------------------------------------------

    @abstractmethod
    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        """
        Run the skill.

        Args:
            ctx:    Runtime context (state store, event bus, secrets …)
            params: Skill-specific parameters provided by the caller

        Returns:
            SkillResult with success flag, output, and optional metadata
        """

    # ------------------------------------------------------------------
    # Lifecycle hooks (optional overrides)
    # ------------------------------------------------------------------

    async def on_load(self) -> None:
        """Called once when the skill is registered. Override for setup."""

    async def on_unload(self) -> None:
        """Called when the skill is removed from the registry. Override for teardown."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def validate_params(self, params: dict[str, Any], required: list[str]) -> str | None:
        """
        Check that all *required* keys exist in *params*.
        Returns an error string if validation fails, None otherwise.
        """
        missing = [k for k in required if k not in params]
        if missing:
            return f"Missing required parameters: {', '.join(missing)}"
        return None

    def __repr__(self) -> str:
        return f"<Skill {self.name!r} v{self.version}>"
