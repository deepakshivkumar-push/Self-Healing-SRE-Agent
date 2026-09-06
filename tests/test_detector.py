from self_healing_sre_agent.detector import ZScoreAnomalyDetector
from self_healing_sre_agent.models import MetricEvent


def test_detector_flags_outlier_after_baseline() -> None:
    detector = ZScoreAnomalyDetector(window_size=10, min_samples=5, threshold=2.0)

    for _ in range(6):
        anomaly = detector.evaluate(
            MetricEvent(name="cpu_usage", value=50.0, unit="percent", source="test")
        )
        assert anomaly is None

    anomaly = detector.evaluate(
        MetricEvent(name="cpu_usage", value=95.0, unit="percent", source="test")
    )

    assert anomaly is not None
    assert anomaly.metric.name == "cpu_usage"
    assert anomaly.score >= 2.0
