from __future__ import annotations

import logging
import time

from .config import Settings
from .detector import ZScoreAnomalyDetector
from .ingestion import SyntheticMetricIngestor
from .remediation import RemediationRouter, SafeMockHandler


def _build_router() -> RemediationRouter:
    router = RemediationRouter()
    router.register("cpu_usage", SafeMockHandler("scale_service", "api"))
    router.register("request_latency", SafeMockHandler("restart_pod", "frontend"))
    return router


def run_service(settings: Settings) -> None:
    logger = logging.getLogger(settings.service_name)
    detector = ZScoreAnomalyDetector(
        window_size=settings.anomaly_window_size,
        min_samples=settings.anomaly_min_samples,
        threshold=settings.anomaly_zscore_threshold,
        std_epsilon=settings.anomaly_std_epsilon,
    )
    ingestor = SyntheticMetricIngestor(seed=42)
    router = _build_router()

    logger.info("service_started demo_mode=%s", settings.demo_mode)

    for i, metrics in enumerate(ingestor.stream(), start=1):
        for metric in metrics:
            logger.info(
                "metric_received metric=%s value=%.3f unit=%s source=%s",
                metric.name,
                metric.value,
                metric.unit,
                metric.source,
            )
            anomaly = detector.evaluate(metric)
            if anomaly is None:
                continue

            logger.warning(
                "anomaly_detected metric=%s score=%.3f severity=%s reason=%s",
                anomaly.metric.name,
                anomaly.score,
                anomaly.severity.value,
                anomaly.reason,
            )
            result = router.dispatch(anomaly, allow_live=settings.allow_live_remediation)
            logger.info(
                "remediation_outcome action=%s target=%s status=%s dry_run=%s message=%s",
                result.action.name,
                result.action.target,
                result.status.value,
                result.action.dry_run,
                result.message,
            )

        if settings.max_iterations > 0 and i >= settings.max_iterations:
            logger.info("service_stopped reason=max_iterations")
            break
        time.sleep(settings.polling_interval_seconds)
