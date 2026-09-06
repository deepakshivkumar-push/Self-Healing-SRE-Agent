from self_healing_sre_agent.models import AnomalyEvent, MetricEvent, Severity
from self_healing_sre_agent.remediation import RemediationRouter, SafeMockHandler


def _anomaly(metric_name: str) -> AnomalyEvent:
    metric = MetricEvent(name=metric_name, value=90.0, unit="percent", source="test")
    return AnomalyEvent(
        metric=metric,
        score=3.2,
        threshold=2.5,
        severity=Severity.high,
        reason="threshold exceeded",
    )


def test_router_uses_handler_with_dry_run_by_default() -> None:
    router = RemediationRouter()
    router.register("cpu_usage", SafeMockHandler("scale_service", "api"))

    result = router.dispatch(_anomaly("cpu_usage"), allow_live=False)

    assert result.status.value == "skipped"
    assert result.action.dry_run is True


def test_router_returns_noop_when_handler_missing() -> None:
    router = RemediationRouter()

    result = router.dispatch(_anomaly("request_latency"), allow_live=False)

    assert result.status.value == "skipped"
    assert result.action.name == "no_op"
