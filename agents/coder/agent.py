"""
CoderAgent — writes, reads, and patches code in the project.

Handles steps dispatched with assigned_role="coder".

Capabilities:
  • Read a file and return its contents
  • Write / overwrite a file with new content
  • Apply a unified diff patch to a file
  • Ask Claude to generate or modify code given a description
  • Ask Claude to review a file and suggest improvements

Event contract
--------------
Listens on:
  step.dispatched  (filters for assigned_role == "coder")

Emits:
  step.completed   payload: {job_id, step_id, result}
  step.failed      payload: {job_id, step_id, error}

Step params schema
------------------
For direct skill use (no LLM):
  action  : "read" | "write" | "list" | "exists" | "delete"
  path    : str
  content : str   (write only)

For LLM-assisted coding:
  action  : "generate" | "review" | "patch"
  path    : str           (file to generate into / review / patch)
  prompt  : str           (what to do)
  diff    : str           (patch only — unified diff string)
"""

from __future__ import annotations

import difflib
import logging
from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_MAX_FILE_BYTES = 256 * 1024
_MAX_CONTEXT_CHARS = 40_000

_SYSTEM_PROMPT = """\
You are the Coder agent for Mission Control, an AI-powered GPU computing platform.
Your job is to write clean, correct, idiomatic Python code.

Guidelines:
- Follow existing project conventions (PEP 8, type hints, async-first)
- Prefer editing the minimal necessary lines
- Do NOT include markdown fences or explanation prose unless asked
- When generating a complete file, output ONLY the file content
- When patching, output ONLY a unified diff (--- / +++ / @@ format)
"""


class CoderAgent(BaseAgent):
    role = "coder"
    capabilities = ["file_manager", "read", "write", "patch", "generate"]

    def __init__(self, *, llm_client: Any = None, llm_model: str = "claude-opus-4-5", **kwargs):
        super().__init__(**kwargs)
        self._llm = llm_client
        self._llm_model = llm_model

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("step.dispatched", self._on_step_dispatched)
        logger.info("[%s] CoderAgent ready", self.agent_id)

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    async def _on_step_dispatched(self, event: Event) -> None:
        payload = event.payload
        if payload.get("assigned_role") != self.role:
            return

        job_id = payload.get("job_id", "")
        step_id = payload.get("step_id", "")
        skill = payload.get("skill", "")
        params = payload.get("params", {})
        description = payload.get("description", "")

        try:
            result = await self._handle(skill, params, description)
            await self.publish("step.completed", {
                "job_id": job_id,
                "step_id": step_id,
                "result": result,
            })
        except Exception as exc:
            logger.exception("[%s] Error handling step %s: %s", self.agent_id, step_id, exc)
            await self.publish("step.failed", {
                "job_id": job_id,
                "step_id": step_id,
                "error": str(exc),
            })

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _handle(self, skill: str, params: dict[str, Any], description: str) -> Any:
        action = params.get("action", "")

        # Direct file-manager skill (no LLM)
        if skill == "file_manager" or action in ("read", "write", "list", "exists", "delete"):
            return await self._file_op(action, params)

        # LLM-assisted actions
        if action == "generate":
            return await self._generate(params, description)
        if action == "review":
            return await self._review(params, description)
        if action == "patch":
            return await self._patch(params)

        # Fallback: treat description as a free-form coding task
        return await self._generate(params, description)

    # ------------------------------------------------------------------
    # Direct file operations (via skill)
    # ------------------------------------------------------------------

    async def _file_op(self, action: str, params: dict[str, Any]) -> Any:
        op = action or params.get("action", "read")
        path = params.get("path", "")
        skill_params: dict[str, Any] = {"action": op, "path": path}
        if op == "write":
            skill_params["content"] = params.get("content", "")

        result = await self.run_skill("file_manager", skill_params)
        if not result.success:
            raise RuntimeError(result.error)
        return result.output

    # ------------------------------------------------------------------
    # LLM: generate code
    # ------------------------------------------------------------------

    async def _generate(self, params: dict[str, Any], description: str) -> str:
        if not self._llm:
            raise RuntimeError("No LLM client configured for CoderAgent")

        path = params.get("path", "")
        prompt = params.get("prompt", description)

        # Optionally include existing file as context
        existing = ""
        if path:
            try:
                existing = self._read_file(path)
            except OSError:
                pass

        user_msg = prompt
        if existing:
            user_msg = f"Existing file `{path}`:\n```\n{existing[:_MAX_CONTEXT_CHARS]}\n```\n\n{prompt}"

        response = self._llm.messages.create(
            model=self._llm_model,
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        code = response.content[0].text.strip()

        # Auto-write if a path was given
        if path:
            target = (Path(self.project_root) / path).resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(code, encoding="utf-8")
            logger.info("[%s] Wrote generated code to %s", self.agent_id, path)
            return f"Generated and written to {path} ({len(code)} chars)"

        return code

    # ------------------------------------------------------------------
    # LLM: review code
    # ------------------------------------------------------------------

    async def _review(self, params: dict[str, Any], description: str) -> str:
        if not self._llm:
            raise RuntimeError("No LLM client configured for CoderAgent")

        path = params.get("path", "")
        prompt = params.get("prompt", description) or "Review this code and suggest improvements."

        if not path:
            raise RuntimeError("review action requires a 'path' parameter")

        content = self._read_file(path)
        user_msg = (
            f"File: `{path}`\n```python\n{content[:_MAX_CONTEXT_CHARS]}\n```\n\n{prompt}"
        )

        response = self._llm.messages.create(
            model=self._llm_model,
            max_tokens=2048,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text.strip()

    # ------------------------------------------------------------------
    # Apply unified diff
    # ------------------------------------------------------------------

    async def _patch(self, params: dict[str, Any]) -> str:
        path = params.get("path", "")
        diff_text = params.get("diff", "")

        if not path:
            raise RuntimeError("patch action requires a 'path' parameter")
        if not diff_text:
            raise RuntimeError("patch action requires a 'diff' parameter")

        original = self._read_file(path)
        original_lines = original.splitlines(keepends=True)

        patched_lines = list(
            difflib.restore(
                difflib.unified_diff([], []),  # sentinel — we parse manually below
                2,
            )
        )

        # Parse unified diff manually (handles --- / +++ / @@ / +/- lines)
        patched_lines = _apply_unified_diff(original_lines, diff_text)
        patched = "".join(patched_lines)

        target = (Path(self.project_root) / path).resolve()
        target.write_text(patched, encoding="utf-8")
        logger.info("[%s] Patched %s", self.agent_id, path)
        return f"Patched {path} ({len(original_lines)} → {len(patched_lines)} lines)"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _read_file(self, path: str) -> str:
        target = (Path(self.project_root) / path).resolve()
        # Path traversal guard
        try:
            target.relative_to(Path(self.project_root).resolve())
        except ValueError:
            raise RuntimeError(f"Path {path!r} escapes project root")
        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if target.stat().st_size > _MAX_FILE_BYTES:
            raise RuntimeError(f"File too large to read: {path}")
        return target.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Unified diff application
# ---------------------------------------------------------------------------

def _apply_unified_diff(original: list[str], diff_text: str) -> list[str]:
    """
    Apply a unified diff string to *original* lines.
    Returns the patched list of lines.
    Raises RuntimeError on malformed patch.
    """
    result = list(original)
    diff_lines = diff_text.splitlines(keepends=True)
    i = 0
    offset = 0   # cumulative line shift from previous hunks

    while i < len(diff_lines):
        line = diff_lines[i]

        # Skip file headers
        if line.startswith("---") or line.startswith("+++"):
            i += 1
            continue

        # Hunk header: @@ -start,count +start,count @@
        if line.startswith("@@"):
            import re
            m = re.search(r"-(\d+)(?:,(\d+))?", line)
            if not m:
                i += 1
                continue
            orig_start = int(m.group(1)) - 1   # 0-indexed
            i += 1
            pos = orig_start + offset
            hunk_orig: list[str] = []
            hunk_new: list[str] = []

            while i < len(diff_lines) and not diff_lines[i].startswith("@@"):
                dl = diff_lines[i]
                if dl.startswith("-"):
                    hunk_orig.append(dl[1:])
                elif dl.startswith("+"):
                    hunk_new.append(dl[1:])
                elif dl.startswith(" "):
                    hunk_orig.append(dl[1:])
                    hunk_new.append(dl[1:])
                elif dl.startswith("---") or dl.startswith("+++"):
                    break
                i += 1

            # Replace the original slice with the new lines
            result[pos : pos + len(hunk_orig)] = hunk_new
            offset += len(hunk_new) - len(hunk_orig)
        else:
            i += 1

    return result
