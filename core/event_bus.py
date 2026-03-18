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
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Awaitable
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
    sequence: int = 0  # assigned by EventBus on publish


Handler = Callable[[Event], Awaitable[None]]


@dataclass
class DeadLetter:
    """A failed event + context stored in the dead letter queue."""
    event: Event
    handler_name: str
    error: str
    timestamp: float = field(default_factory=time.time)
    attempts: int = 1


class EventBus:
    """
    Pub/sub event bus.  Automatically uses Redis Streams when available,
    falls back to in-process asyncio queues otherwise.

    Dead Letter Queue:
      - Failed handler invocations are stored in a bounded deque (max 500)
      - Access via bus.dead_letters (list) and bus.dead_letter_count (int)
      - Handlers get up to 2 retry attempts with 0.5s backoff before DLQ
    """

    _MAX_DLQ_SIZE = 500
    _MAX_HANDLER_RETRIES = 2
    _RETRY_BACKOFF = 0.5  # seconds

    _REPLAY_BUFFER_SIZE = 200

    def __init__(self, redis_url: str | None = None):
        self._redis_url = redis_url
        self._redis: object | None = None
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._mode = "memory"
        self._running = False
        self._dlq: deque[DeadLetter] = deque(maxlen=self._MAX_DLQ_SIZE)
        self._seq_counter = 0
        self._seq_lock = threading.Lock()
        self._replay_buffer: deque[Event] = deque(maxlen=self._REPLAY_BUFFER_SIZE)

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
        with self._seq_lock:
            self._seq_counter += 1
            event.sequence = self._seq_counter
        self._replay_buffer.append(event)

        if self._mode == "redis" and self._redis:
            await self._publish_redis(event)
        else:
            await self._queue.put(event)
        logger.debug("Published event: %s [seq=%d]", event.event_type, event.sequence)

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
                    await self._invoke_handler(handler, event)

    async def _invoke_handler(self, handler: Handler, event: Event) -> None:
        """Invoke a handler with retry logic; dead-letter on exhaustion."""
        last_exc: Exception | None = None
        for attempt in range(1, self._MAX_HANDLER_RETRIES + 1):
            try:
                await handler(event)
                return  # success
            except Exception as exc:
                last_exc = exc
                logger.warning(
                    "Handler %s failed (attempt %d/%d) for event %s: %s",
                    handler.__name__, attempt, self._MAX_HANDLER_RETRIES,
                    event.event_type, exc,
                )
                if attempt < self._MAX_HANDLER_RETRIES:
                    await asyncio.sleep(self._RETRY_BACKOFF * attempt)

        # All retries exhausted — send to dead letter queue
        dl = DeadLetter(
            event=event,
            handler_name=handler.__name__,
            error=str(last_exc),
            attempts=self._MAX_HANDLER_RETRIES,
        )
        self._dlq.append(dl)
        logger.error(
            "Handler %s dead-lettered for event %s after %d attempts: %s",
            handler.__name__, event.event_type, self._MAX_HANDLER_RETRIES, last_exc,
        )

    # ------------------------------------------------------------------
    # Dead Letter Queue API
    # ------------------------------------------------------------------

    @property
    def dead_letters(self) -> list[DeadLetter]:
        """Return all dead-lettered events (most recent last)."""
        return list(self._dlq)

    @property
    def dead_letter_count(self) -> int:
        return len(self._dlq)

    def clear_dead_letters(self) -> int:
        """Clear the DLQ. Returns the number of entries cleared."""
        count = len(self._dlq)
        self._dlq.clear()
        return count

    # ------------------------------------------------------------------
    # Replay buffer API
    # ------------------------------------------------------------------

    def replay_since(self, sequence: int) -> list[Event]:
        """Return all buffered events with sequence > *sequence*."""
        return [e for e in self._replay_buffer if e.sequence > sequence]

    @property
    def last_sequence(self) -> int:
        """Return the most recently assigned sequence number."""
        return self._seq_counter

    @property
    def mode(self) -> str:
        return self._mode
