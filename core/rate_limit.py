"""
In-memory sliding-window rate limiter for FastAPI.

Usage in main.py:
    from core.rate_limit import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

Behaviour:
    - Tracks requests per client IP using a sliding window
    - Returns 429 Too Many Requests when limit is exceeded
    - Configurable via MC_RATE_LIMIT env var (requests per minute, default 60)
    - Separate (lower) limit for expensive endpoints like /chat/stream
    - Public/static paths are not rate-limited
"""

from __future__ import annotations

import os
import time
from collections import defaultdict
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Default: 60 requests per minute per IP
_DEFAULT_RPM = int(os.getenv("MC_RATE_LIMIT", "60"))
_WINDOW_SECONDS = 60

# Expensive endpoints get a lower limit (1/3 of normal)
_EXPENSIVE_PATHS = frozenset({"/chat", "/chat/stream", "/tasks"})

# Paths exempt from rate limiting
_EXEMPT_PATHS = frozenset({"/", "/mobile", "/docs", "/openapi.json", "/redoc", "/events"})


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding-window rate limiter keyed by client IP."""

    def __init__(self, app, requests_per_minute: int = _DEFAULT_RPM):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.expensive_rpm = max(requests_per_minute // 3, 5)
        # ip → list of timestamps
        self._windows: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path

        # Skip exempt paths
        if path in _EXEMPT_PATHS:
            return await call_next(request)

        # Determine client IP
        client_ip = request.client.host if request.client else "unknown"

        # Choose limit based on endpoint
        if any(path.startswith(p) for p in _EXPENSIVE_PATHS):
            limit = self.expensive_rpm
            key = f"{client_ip}:expensive"
        else:
            limit = self.rpm
            key = client_ip

        now = time.monotonic()
        window = self._windows[key]

        # Prune timestamps outside the sliding window
        cutoff = now - _WINDOW_SECONDS
        self._windows[key] = window = [t for t in window if t > cutoff]

        if len(window) >= limit:
            retry_after = int(window[0] - cutoff) + 1
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Slow down.",
                    "retry_after_seconds": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )

        window.append(now)
        return await call_next(request)
