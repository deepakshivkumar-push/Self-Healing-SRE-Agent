from __future__ import annotations

import statistics
from collections import defaultdict, deque

from .models import AnomalyEvent, MetricEvent, Severity


class ZScoreAnomalyDetector:
    def __init__(
        self,
        window_size: int = 20,
        min_samples: int = 8,
        threshold: float = 2.5,
        std_epsilon: float = 0.001,
    ) -> None:
        self.window_size = window_size
        self.min_samples = min_samples
        self.threshold = threshold
        self.std_epsilon = std_epsilon
        self._history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=self.window_size))

    def evaluate(self, metric: MetricEvent) -> AnomalyEvent | None:
        history = self._history[metric.name]
        if len(history) >= self.min_samples:
            mean = statistics.fmean(history)
            std = statistics.pstdev(history)
            z_score = abs(metric.value - mean) / max(std, self.std_epsilon) if history else 0.0
            if z_score >= self.threshold:
                severity = Severity.critical if z_score >= self.threshold * 2 else Severity.high
                event = AnomalyEvent(
                    metric=metric,
                    score=round(z_score, 3),
                    threshold=self.threshold,
                    severity=severity,
                    reason=(
                        f"z-score {z_score:.2f} exceeded threshold "
                        f"{self.threshold:.2f} for {metric.name}"
                    ),
                )
                history.append(metric.value)
                return event

        history.append(metric.value)
        return None
