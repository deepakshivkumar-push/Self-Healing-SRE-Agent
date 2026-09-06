from __future__ import annotations

import random
from collections.abc import Iterator

from .models import MetricEvent


class SyntheticMetricIngestor:
    """Synthetic stream with periodic CPU and latency spikes."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._tick = 0

    def stream(self) -> Iterator[list[MetricEvent]]:
        while True:
            self._tick += 1
            cpu_value = self._rng.uniform(30, 55)
            latency_value = self._rng.uniform(120, 220)

            if self._tick % 13 == 0:
                cpu_value = self._rng.uniform(90, 98)
            if self._tick % 17 == 0:
                latency_value = self._rng.uniform(450, 700)

            yield [
                MetricEvent(name="cpu_usage", value=cpu_value, unit="percent", source="demo"),
                MetricEvent(
                    name="request_latency",
                    value=latency_value,
                    unit="ms",
                    source="demo",
                ),
            ]
