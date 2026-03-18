"""
Structured logging — JSON-formatted logs with correlation context.

Uses Python's contextvars to automatically attach job_id, step_id,
agent_id, and correlation_id to every log record within a request scope.

Usage:
    from core.logging import configure_logging, set_log_context, clear_log_context

    configure_logging()  # call once at startup

    # In agent/handler code:
    set_log_context(agent_id="coder-1", job_id="abc", step_id="s1")
    logger.info("Processing step")  # auto-includes context fields
    clear_log_context()

Env vars:
    LOG_LEVEL   — DEBUG, INFO, WARNING, ERROR (default: INFO)
    LOG_FORMAT  — json or text (default: text)
"""

from __future__ import annotations

import json
import logging
import os
import time
from contextvars import ContextVar
from typing import Any

# Context variables for request-scoped correlation
_ctx_agent_id: ContextVar[str] = ContextVar("agent_id", default="")
_ctx_job_id: ContextVar[str] = ContextVar("job_id", default="")
_ctx_step_id: ContextVar[str] = ContextVar("step_id", default="")
_ctx_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def set_log_context(
    *,
    agent_id: str = "",
    job_id: str = "",
    step_id: str = "",
    correlation_id: str = "",
) -> None:
    """Set correlation context for the current async task / thread."""
    if agent_id:
        _ctx_agent_id.set(agent_id)
    if job_id:
        _ctx_job_id.set(job_id)
    if step_id:
        _ctx_step_id.set(step_id)
    if correlation_id:
        _ctx_correlation_id.set(correlation_id)


def clear_log_context() -> None:
    """Reset all correlation context."""
    _ctx_agent_id.set("")
    _ctx_job_id.set("")
    _ctx_step_id.set("")
    _ctx_correlation_id.set("")


def get_log_context() -> dict[str, str]:
    """Return the current correlation context as a dict (non-empty values only)."""
    ctx: dict[str, str] = {}
    if v := _ctx_agent_id.get():
        ctx["agent_id"] = v
    if v := _ctx_job_id.get():
        ctx["job_id"] = v
    if v := _ctx_step_id.get():
        ctx["step_id"] = v
    if v := _ctx_correlation_id.get():
        ctx["correlation_id"] = v
    return ctx


class StructuredFormatter(logging.Formatter):
    """JSON log formatter that includes correlation context."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach correlation context
        ctx = get_log_context()
        if ctx:
            entry.update(ctx)

        # Include exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(entry, default=str)


class ContextFormatter(logging.Formatter):
    """Human-readable formatter that appends correlation context."""

    def __init__(self, fmt: str | None = None, **kwargs):
        super().__init__(fmt or "%(asctime)s %(levelname)-8s %(name)s — %(message)s", **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        ctx = get_log_context()
        if ctx:
            ctx_str = " ".join(f"{k}={v}" for k, v in ctx.items())
            return f"{base}  [{ctx_str}]"
        return base


def configure_logging(
    level: str | None = None,
    log_format: str | None = None,
) -> None:
    """Configure Python logging for the application.

    Args:
        level:      LOG_LEVEL override (default from env or INFO)
        log_format: "json" or "text" (default from env or text)
    """
    level = level or os.getenv("LOG_LEVEL", "INFO")
    log_format = log_format or os.getenv("LOG_FORMAT", "text")

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates on reconfigure
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handler = logging.StreamHandler()
    if log_format.lower() == "json":
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(ContextFormatter())

    root.addHandler(handler)

    # Quiet noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
