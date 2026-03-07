"""
Built-in skill: file_manager

Provides safe file operations within an allowed base directory.

Supported actions:
  read    — return file contents as a string
  write   — write string content to a file (creates parent dirs)
  list    — list files/dirs at a path (non-recursive)
  exists  — check if a path exists
  delete  — delete a file (not directories)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

# Files larger than this are refused (safety guard)
_MAX_READ_BYTES = 512 * 1024  # 512 KB


class FileManagerSkill(BaseSkill):
    name = "file_manager"
    description = "Read, write, list, and delete files within the project directory"
    version = "0.1.0"

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "")
        path_str = params.get("path", "")

        if not action:
            return SkillResult.fail("Missing required parameter: action")
        if not path_str:
            return SkillResult.fail("Missing required parameter: path")

        # Resolve path relative to project root from ctx metadata
        base_dir = Path(ctx.metadata.get("project_root", ".")).resolve()
        target = (base_dir / path_str).resolve()

        # Safety: prevent path traversal outside base_dir
        try:
            target.relative_to(base_dir)
        except ValueError:
            return SkillResult.fail(
                f"Path {path_str!r} escapes the allowed base directory"
            )

        try:
            if action == "read":
                return await self._read(target)
            elif action == "write":
                return await self._write(target, params.get("content", ""))
            elif action == "list":
                return await self._list(target)
            elif action == "exists":
                return SkillResult.ok(output=target.exists())
            elif action == "delete":
                return await self._delete(target)
            else:
                return SkillResult.fail(
                    f"Unknown action {action!r}. Choose: read, write, list, exists, delete"
                )
        except Exception as exc:
            logger.exception("file_manager error: %s", exc)
            return SkillResult.fail(str(exc))

    # ------------------------------------------------------------------

    async def _read(self, path: Path) -> SkillResult:
        if not path.exists():
            return SkillResult.fail(f"File not found: {path}")
        if not path.is_file():
            return SkillResult.fail(f"Path is not a file: {path}")
        size = path.stat().st_size
        if size > _MAX_READ_BYTES:
            return SkillResult.fail(
                f"File too large ({size} bytes). Limit is {_MAX_READ_BYTES} bytes."
            )
        content = path.read_text(encoding="utf-8", errors="replace")
        return SkillResult.ok(output=content, size_bytes=size)

    async def _write(self, path: Path, content: str) -> SkillResult:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return SkillResult.ok(output=str(path), size_bytes=len(content.encode()))

    async def _list(self, path: Path) -> SkillResult:
        if not path.exists():
            return SkillResult.fail(f"Path not found: {path}")
        if path.is_file():
            return SkillResult.ok(output=[path.name])
        entries = [
            {"name": e.name, "type": "dir" if e.is_dir() else "file"}
            for e in sorted(path.iterdir())
        ]
        return SkillResult.ok(output=entries, count=len(entries))

    async def _delete(self, path: Path) -> SkillResult:
        if not path.exists():
            return SkillResult.fail(f"File not found: {path}")
        if not path.is_file():
            return SkillResult.fail("delete only supports files, not directories")
        path.unlink()
        return SkillResult.ok(output=f"Deleted: {path}")
