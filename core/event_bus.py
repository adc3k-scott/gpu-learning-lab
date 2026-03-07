"""
Event bus — dual mode.
  • In-memory (default): asyncio queues, works with no external dependencies.
  • Redis mode: activates automatically when REDIS_URL is set and redis is reachable.

Usage:
    bus = EventBus()
    await bus.connect()

    bus.subscribe("job.*", my_handler)          # wildcard support
    await bus.publish(Event(event_type="job.started", payload={"id": "abc"}))
"""

from __future__ import annotations

import asyncio
import fnmatch
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Awaitable
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass
class Event:
    event_type: str
    payload: dict = field(default_factory=dict)
    source: str = ""
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


Handler = Callable[[Event], Awaitable[None]]


class EventBus:
    """
    Pub/sub event bus.  Automatically uses Redis Streams when available,
    falls back to in-process asyncio queues otherwise.
    """

    def __init__(self, redis_url: str | None = None):
        self._redis_url = redis_url
        self._redis: object | None = None
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._mode = "memory"
        self._running = False

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
                logger.info("EventBus connected to Redis at %s", self._redis_url)
            except Exception as exc:
                logger.warning(
                    "Redis unavailable (%s) — falling back to in-memory event bus", exc
                )
        else:
            logger.info("EventBus running in-memory mode (no REDIS_URL configured)")

        self._running = True
        asyncio.create_task(self._dispatch_loop())

    async def disconnect(self) -> None:
        self._running = False
        if self._redis:
            await self._redis.aclose()  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def subscribe(self, pattern: str, handler: Handler) -> None:
        """
        Register a coroutine handler for events matching *pattern*.
        Supports shell-style wildcards: "job.*", "*.failed", "*".
        """
        self._handlers[pattern].append(handler)
        logger.debug("Subscribed handler %s to pattern '%s'", handler.__name__, pattern)

    def unsubscribe(self, pattern: str, handler: Handler) -> None:
        self._handlers[pattern] = [
            h for h in self._handlers[pattern] if h is not handler
        ]

    async def publish(self, event: Event) -> None:
        if self._mode == "redis" and self._redis:
            await self._publish_redis(event)
        else:
            await self._queue.put(event)
        logger.debug("Published event: %s [%s]", event.event_type, event.event_id)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _publish_redis(self, event: Event) -> None:
        import json

        data = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "correlation_id": event.correlation_id,
            "timestamp": event.timestamp,
            "payload": json.dumps(event.payload),
        }
        await self._redis.xadd(f"events:{event.event_type}", data)  # type: ignore[attr-defined]
        # Also push to local queue so in-process subscribers get it
        await self._queue.put(event)

    async def _dispatch_loop(self) -> None:
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=0.1)
                await self._dispatch(event)
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as exc:
                logger.exception("Error in event dispatch loop: %s", exc)

    async def _dispatch(self, event: Event) -> None:
        for pattern, handlers in self._handlers.items():
            if fnmatch.fnmatch(event.event_type, pattern):
                for handler in handlers:
                    try:
                        await handler(event)
                    except Exception as exc:
                        logger.exception(
                            "Handler %s failed for event %s: %s",
                            handler.__name__,
                            event.event_type,
                            exc,
                        )

    @property
    def mode(self) -> str:
        return self._mode
