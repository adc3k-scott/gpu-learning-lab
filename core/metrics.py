"""
In-memory metrics collector for Mission Control observability.

Provides counters, gauges, histograms (timing), and a snapshot API.
No external dependencies — designed for the /metrics endpoint and
dashboard consumption.

Usage:
    from core.metrics import metrics

    metrics.increment("skills.executed")
    metrics.timing("skills.file_manager.duration_ms", 42.3)
    metrics.gauge("agents.running", 6)

    snapshot = metrics.snapshot()  # → dict of all metrics
"""

from __future__ import annotations

import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class _HistogramBucket:
    """Accumulates timing samples with basic statistics."""
    count: int = 0
    total: float = 0.0
    min_val: float = float("inf")
    max_val: float = float("-inf")
    _recent: list[float] = field(default_factory=list)  # last 100 samples

    def record(self, value: float) -> None:
        self.count += 1
        self.total += value
        if value < self.min_val:
            self.min_val = value
        if value > self.max_val:
            self.max_val = value
        self._recent.append(value)
        if len(self._recent) > 100:
            self._recent.pop(0)

    @property
    def avg(self) -> float:
        return self.total / self.count if self.count else 0.0

    @property
    def p50(self) -> float:
        if not self._recent:
            return 0.0
        s = sorted(self._recent)
        return s[len(s) // 2]

    @property
    def p95(self) -> float:
        if not self._recent:
            return 0.0
        s = sorted(self._recent)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    def to_dict(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "total": round(self.total, 2),
            "avg": round(self.avg, 2),
            "min": round(self.min_val, 2) if self.count else 0,
            "max": round(self.max_val, 2) if self.count else 0,
            "p50": round(self.p50, 2),
            "p95": round(self.p95, 2),
        }


class MetricsCollector:
    """Thread-safe in-memory metrics store."""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: dict[str, int] = defaultdict(int)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, _HistogramBucket] = defaultdict(_HistogramBucket)
        self._started_at = time.time()

    # ------------------------------------------------------------------
    # Counter — monotonically increasing values (request count, errors)
    # ------------------------------------------------------------------

    def increment(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._counters[name] += amount

    def counter(self, name: str) -> int:
        with self._lock:
            return self._counters.get(name, 0)

    # ------------------------------------------------------------------
    # Gauge — point-in-time values (active agents, queue depth)
    # ------------------------------------------------------------------

    def gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def get_gauge(self, name: str) -> float:
        with self._lock:
            return self._gauges.get(name, 0.0)

    # ------------------------------------------------------------------
    # Histogram — timing / distribution data
    # ------------------------------------------------------------------

    def timing(self, name: str, value_ms: float) -> None:
        with self._lock:
            self._histograms[name].record(value_ms)

    def timer(self, name: str) -> "_Timer":
        """Context manager that records elapsed time in milliseconds."""
        return _Timer(self, name)

    # ------------------------------------------------------------------
    # Snapshot — full dump for API endpoint
    # ------------------------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "uptime_seconds": round(time.time() - self._started_at, 1),
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {k: v.to_dict() for k, v in self._histograms.items()},
            }

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._started_at = time.time()


class _Timer:
    """Context manager for timing blocks of code."""

    def __init__(self, collector: MetricsCollector, name: str):
        self._collector = collector
        self._name = name
        self._start: float = 0

    def __enter__(self) -> "_Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args) -> None:
        elapsed_ms = (time.perf_counter() - self._start) * 1000
        self._collector.timing(self._name, elapsed_ms)

    async def __aenter__(self) -> "_Timer":
        self._start = time.perf_counter()
        return self

    async def __aexit__(self, *args) -> None:
        elapsed_ms = (time.perf_counter() - self._start) * 1000
        self._collector.timing(self._name, elapsed_ms)


# Singleton — import and use everywhere
metrics = MetricsCollector()
