"""
State store — dual mode.
  • In-memory (default): plain dict, works with no external dependencies.
  • Redis mode: activates automatically when REDIS_URL is set and redis is reachable.

Usage:
    store = StateStore()
    await store.connect()

    await store.set("jobs:abc", {"status": "running"}, ttl=3600)
    data = await store.get("jobs:abc")
    await store.delete("jobs:abc")
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class StateStore:
    """
    Key-value state store.  Uses Redis when available, in-process dict otherwise.
    All values are JSON-serialised so the interface is identical in both modes.
    """

    def __init__(self, redis_url: str | None = None):
        self._redis_url = redis_url
        self._redis: object | None = None
        self._store: dict[str, tuple[str, float | None]] = {}  # key → (json, expires_at)
        self._mode = "memory"
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        if self._redis_url:
            try:
                import redis.asyncio as aioredis  # type: ignore

                client = aioredis.from_url(self._redis_url, decode_responses=True)
                await client.ping()
                self._redis = client
                self._mode = "redis"
                logger.info("StateStore connected to Redis at %s", self._redis_url)
            except Exception as exc:
                logger.warning(
                    "Redis unavailable (%s) — falling back to in-memory state store", exc
                )
        else:
            logger.info("StateStore running in-memory mode (no REDIS_URL configured)")

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.aclose()  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Store *value* under *key*.  Optional *ttl* in seconds."""
        serialised = json.dumps(value)
        if self._mode == "redis" and self._redis:
            if ttl:
                await self._redis.setex(key, ttl, serialised)  # type: ignore[attr-defined]
            else:
                await self._redis.set(key, serialised)  # type: ignore[attr-defined]
        else:
            expires_at = time.monotonic() + ttl if ttl else None
            async with self._lock:
                self._store[key] = (serialised, expires_at)

    async def get(self, key: str) -> Any | None:
        """Return the value for *key*, or None if missing / expired."""
        if self._mode == "redis" and self._redis:
            raw = await self._redis.get(key)  # type: ignore[attr-defined]
            return json.loads(raw) if raw is not None else None
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            serialised, expires_at = entry
            if expires_at is not None and time.monotonic() > expires_at:
                del self._store[key]
                return None
            return json.loads(serialised)

    async def delete(self, key: str) -> None:
        if self._mode == "redis" and self._redis:
            await self._redis.delete(key)  # type: ignore[attr-defined]
        else:
            async with self._lock:
                self._store.pop(key, None)

    async def exists(self, key: str) -> bool:
        if self._mode == "redis" and self._redis:
            return bool(await self._redis.exists(key))  # type: ignore[attr-defined]
        async with self._lock:
            return key in self._store

    async def keys(self, pattern: str = "*") -> list[str]:
        """Return all keys matching *pattern* (shell-style glob)."""
        import fnmatch

        if self._mode == "redis" and self._redis:
            return await self._redis.keys(pattern)  # type: ignore[attr-defined]
        async with self._lock:
            now = time.monotonic()
            return [
                k
                for k, (_, exp) in self._store.items()
                if (exp is None or now <= exp) and fnmatch.fnmatch(k, pattern)
            ]

    async def get_all(self, pattern: str = "*") -> dict[str, Any]:
        """Return a dict of all matching key → deserialized value pairs."""
        result = {}
        for key in await self.keys(pattern):
            val = await self.get(key)
            if val is not None:
                result[key] = val
        return result

    @property
    def mode(self) -> str:
        return self._mode
