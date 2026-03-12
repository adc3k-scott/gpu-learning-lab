"""
Secret masking and error sanitisation utilities.

Used to prevent API keys, tokens, and other sensitive values from leaking
into error messages, log output, or HTTP responses.
"""

from __future__ import annotations

import os
import re

# ---------------------------------------------------------------------------
# Secret registry — values to mask in any output
# ---------------------------------------------------------------------------

# Env var names that hold secrets (values will be collected at mask time)
_SECRET_ENV_VARS = [
    "ANTHROPIC_API_KEY",
    "RUNPOD_API_KEY",
    "NOTION_API_KEY",
    "MC_API_KEY",
    "REDIS_URL",
    "PEXELS_API_KEY",
]

# Regex for common secret patterns (Bearer tokens, sk-* keys, etc.)
_SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),          # Anthropic / OpenAI keys
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-./+=]{20,}"),  # Bearer tokens
    re.compile(r"token[=:\s]+[a-zA-Z0-9_\-./+=]{20,}", re.I),
    re.compile(r"key[=:\s]+[a-zA-Z0-9_\-./+=]{20,}", re.I),
    re.compile(r"secret[=:\s]+[a-zA-Z0-9_\-./+=]{20,}", re.I),
    re.compile(r"ntn_[a-zA-Z0-9]{20,}"),            # Notion integration tokens
]


def _collect_secrets() -> list[str]:
    """Gather current secret values from environment."""
    secrets = []
    for name in _SECRET_ENV_VARS:
        val = os.environ.get(name, "")
        if val and len(val) >= 8:  # only mask non-trivial values
            secrets.append(val)
    return secrets


def mask_secrets(text: str) -> str:
    """
    Replace any known secret values or patterns in *text* with '[REDACTED]'.

    This is designed to be called on error messages, log strings, and HTTP
    response bodies before they leave the system boundary.
    """
    if not text:
        return text

    # Mask known env var values
    for secret in _collect_secrets():
        if secret in text:
            text = text.replace(secret, "[REDACTED]")

    # Mask pattern-matched secrets
    for pat in _SECRET_PATTERNS:
        text = pat.sub("[REDACTED]", text)

    return text


def safe_error(exc: Exception) -> str:
    """Return a masked string representation of an exception."""
    return mask_secrets(str(exc))
