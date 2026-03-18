"""
Circuit breaker — prevents cascading failures from external services.

Three states:
  CLOSED   — normal operation, requests flow through
  OPEN     — service presumed down, requests fail fast
  HALF_OPEN — probe: allow one request through to test recovery

Transition rules:
  CLOSED → OPEN         when failure_count >= failure_threshold
  OPEN → HALF_OPEN      when cooldown_seconds have elapsed
  HALF_OPEN → CLOSED    when a probe request succeeds
  HALF_OPEN → OPEN      when a probe request fails (resets cooldown)

Usage:
    cb = CircuitBreaker("runpod", failure_threshold=5, cooldown_seconds=60)
    try:
        result = await cb.call(some_coroutine())
    except CircuitOpenError:
        # service is down, fail fast
"""

from __future__ import annotations

import asyncio
import logging
import time
from enum import Enum
from typing import Any, TypeVar

from core.metrics import metrics

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    """Raised when the circuit breaker is open and requests are rejected."""

    def __init__(self, name: str, retry_after: float):
        self.name = name
        self.retry_after = retry_after
        super().__init__(f"Circuit breaker '{name}' is OPEN — retry after {retry_after:.0f}s")


class CircuitBreaker:
    """Per-service circuit breaker with failure counting and cooldown."""

    def __init__(
        self,
        name: str,
        *,
        failure_threshold: int = 5,
        cooldown_seconds: float = 60.0,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0.0
        self._opened_at: float = 0.0

    @property
    def state(self) -> CircuitState:
        """Current state, accounting for automatic OPEN → HALF_OPEN transition."""
        if self._state == CircuitState.OPEN:
            if time.time() - self._opened_at >= self.cooldown_seconds:
                return CircuitState.HALF_OPEN
        return self._state

    @property
    def failure_count(self) -> int:
        return self._failure_count

    async def call(self, coro: Any) -> Any:
        """Execute a coroutine through the circuit breaker.

        Raises CircuitOpenError if the circuit is open.
        On success in HALF_OPEN, transitions to CLOSED.
        On failure, increments failure count and may open the circuit.
        """
        current = self.state

        if current == CircuitState.OPEN:
            retry_after = self.cooldown_seconds - (time.time() - self._opened_at)
            raise CircuitOpenError(self.name, max(retry_after, 0))

        try:
            result = await coro
            self._on_success(current)
            return result
        except Exception:
            self._on_failure(current)
            raise

    def record_success(self) -> None:
        """Manually record a success (for use outside call())."""
        self._on_success(self.state)

    def record_failure(self) -> None:
        """Manually record a failure (for use outside call())."""
        self._on_failure(self.state)

    def reset(self) -> None:
        """Force-reset to CLOSED state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._opened_at = 0.0

    def _on_success(self, state_at_call: CircuitState) -> None:
        if state_at_call == CircuitState.HALF_OPEN:
            logger.info("Circuit breaker '%s' recovered — HALF_OPEN → CLOSED", self.name)
            metrics.increment(f"circuit.{self.name}.recovered")
        self._state = CircuitState.CLOSED
        self._failure_count = 0

    def _on_failure(self, state_at_call: CircuitState) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        metrics.increment(f"circuit.{self.name}.failure")

        if state_at_call == CircuitState.HALF_OPEN:
            # Probe failed — reopen
            self._open()
            return

        if self._failure_count >= self.failure_threshold:
            self._open()

    def _open(self) -> None:
        self._state = CircuitState.OPEN
        self._opened_at = time.time()
        metrics.increment(f"circuit.{self.name}.opened")
        logger.warning(
            "Circuit breaker '%s' OPENED after %d failures (cooldown=%.0fs)",
            self.name, self._failure_count, self.cooldown_seconds,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "failure_threshold": self.failure_threshold,
            "cooldown_seconds": self.cooldown_seconds,
        }
