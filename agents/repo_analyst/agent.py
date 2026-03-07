"""
RepoAnalystAgent — understands and explains the codebase.

Handles steps dispatched with assigned_role="repo_analyst".

Capabilities:
  • List directory contents
  • Read and return file content
  • Build a directory tree of the project
  • Ask Claude to explain / summarise / answer questions about code

Event contract
--------------
Listens on:
  step.dispatched  (filters for assigned_role == "repo_analyst")

Emits:
  step.completed   payload: {job_id, step_id, result}
  step.failed      payload: {job_id, step_id, error}
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}
_TEXT_EXTS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json",
    ".html", ".css", ".js", ".ts", ".sh", ".bat", ".env",
}
_MAX_FILE_BYTES = 256 * 1024   # 256 KB — hard cap per file read
_MAX_CONTEXT_CHARS = 60_000    # total chars sent to Claude per analysis


class RepoAnalystAgent(BaseAgent):
    role = "repo_analyst"

    def __init__(self, *, llm_client: Any = None, llm_model: str = "claude-opus-4-5", **kwargs):
        super().__init__(**kwargs)
        self._llm = llm_client
        self._llm_model = llm_model

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("step.dispatched", self._on_step_dispatched)
        logger.info("[%s] RepoAnalystAgent ready", self.agent_id)

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
    # Dispatch table
    # ------------------------------------------------------------------

    async def _handle(self, skill: str, params: dict[str, Any], description: str) -> Any:
        if skill == "file_manager":
            action = params.get("action", "list")
            path = params.get("path", ".")
            result = await self.run_skill("file_manager", {"action": action, "path": path})
            if not result.success:
                raise RuntimeError(result.error)
            return result.output

        # Everything else: build repo context, ask Claude
        return await self._analyse(description, params)

    # ------------------------------------------------------------------
    # Core analysis: build context + call Claude
    # ------------------------------------------------------------------

    async def _analyse(self, question: str, params: dict[str, Any]) -> str:
        if not self._llm:
            return self._tree(self.project_root)

        focus_path = params.get("path", "")
        context = self._build_context(focus_path)

        system = (
            "You are the Repo Analyst for Mission Control, an AI-powered GPU computing platform. "
            "You have deep knowledge of the repository structure and can explain code, "
            "answer questions about files, and suggest improvements.\n\n"
            f"REPOSITORY CONTEXT:\n{context}"
        )

        response = self._llm.messages.create(
            model=self._llm_model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": question}],
        )
        return response.content[0].text.strip()

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _build_context(self, focus_path: str = "") -> str:
        """Build a compact repo snapshot for the LLM context window."""
        root = Path(self.project_root)
        parts: list[str] = []

        # Directory tree first
        parts.append("=== DIRECTORY TREE ===")
        parts.append(self._tree(str(root)))
        parts.append("")

        # If a specific path was requested, read just that
        if focus_path:
            target = (root / focus_path).resolve()
            try:
                target.relative_to(root)   # path-traversal guard
                if target.is_file():
                    content = target.read_text(encoding="utf-8", errors="replace")
                    parts.append(f"=== {focus_path} ===")
                    parts.append(content[:_MAX_CONTEXT_CHARS])
                    return "\n".join(parts)
            except (ValueError, OSError):
                pass

        # Otherwise include priority files + as many others as fit
        budget = _MAX_CONTEXT_CHARS
        priority = ["README.md", "CLAUDE.md", "pyproject.toml", "main.py"]
        seen: set[str] = set()

        def _add_file(rel: str) -> None:
            nonlocal budget
            if budget <= 0 or rel in seen:
                return
            path = root / rel
            if not path.is_file() or path.suffix not in _TEXT_EXTS:
                return
            try:
                size = path.stat().st_size
                if size > _MAX_FILE_BYTES:
                    return
                text = path.read_text(encoding="utf-8", errors="replace")
                chunk = text[:budget]
                parts.append(f"=== {rel} ===")
                parts.append(chunk)
                parts.append("")
                budget -= len(chunk)
                seen.add(rel)
            except OSError:
                pass

        for name in priority:
            _add_file(name)

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for fname in sorted(filenames):
                rel = os.path.relpath(os.path.join(dirpath, fname), root)
                _add_file(rel)

        return "\n".join(parts)

    def _tree(self, root: str, prefix: str = "", max_depth: int = 4) -> str:
        """Return an ASCII directory tree string."""
        lines: list[str] = [Path(root).name + "/"]

        def _walk(path: Path, pfx: str, depth: int) -> None:
            if depth > max_depth:
                return
            try:
                entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
            except PermissionError:
                return
            entries = [e for e in entries if e.name not in _SKIP_DIRS]
            for i, entry in enumerate(entries):
                connector = "└── " if i == len(entries) - 1 else "├── "
                lines.append(pfx + connector + entry.name + ("/" if entry.is_dir() else ""))
                if entry.is_dir():
                    extension = "    " if i == len(entries) - 1 else "│   "
                    _walk(entry, pfx + extension, depth + 1)

        _walk(Path(root), prefix, 1)
        return "\n".join(lines)
