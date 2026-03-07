"""
Custom skill template — copy this file, rename it (no leading underscore),
and implement the execute() method.

The registry auto-discovers all non-underscore modules in skills/custom/.

Example:
    Copy to:  skills/custom/my_tool.py
    Run with: skill = registry.get("my_tool")
              result = await skill.execute(ctx, {"param": "value"})
"""

from __future__ import annotations

from typing import Any

from skills.base import BaseSkill, RetryPolicy, SkillContext, SkillResult


class MyCustomSkill(BaseSkill):
    # ------------------------------------------------------------------
    # Identity — required
    # ------------------------------------------------------------------
    name = "my_custom_skill"
    description = "One-line description of what this skill does"
    version = "0.1.0"

    # ------------------------------------------------------------------
    # Secrets — list env-var names your skill needs
    # e.g. required_secrets = ["MY_API_KEY"]
    # Access them in execute() via ctx.secrets["MY_API_KEY"]
    # ------------------------------------------------------------------
    required_secrets: list[str] = []

    # ------------------------------------------------------------------
    # Retry — remove if you don't need retries
    # ------------------------------------------------------------------
    retry_policy = RetryPolicy(max_attempts=3, backoff_base=2.0)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def on_load(self) -> None:
        """Called once when skill is registered. Set up connections here."""

    async def on_unload(self) -> None:
        """Called when skill is removed. Close connections here."""

    # ------------------------------------------------------------------
    # Main logic
    # ------------------------------------------------------------------

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        # Validate required params
        error = self.validate_params(params, required=["input"])
        if error:
            return SkillResult.fail(error)

        # Your logic here
        result = params["input"].upper()  # placeholder

        return SkillResult.ok(output=result)
