from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import ActionStatus, AnomalyEvent, RemediationAction, RemediationResult


class Handler(Protocol):
    def execute(self, anomaly: AnomalyEvent, *, allow_live: bool) -> RemediationResult: ...


@dataclass(slots=True)
class SafeMockHandler:
    action_name: str
    target: str

    def execute(self, anomaly: AnomalyEvent, *, allow_live: bool) -> RemediationResult:
        action = RemediationAction(
            name=self.action_name,
            target=self.target,
            dry_run=not allow_live,
            rationale=anomaly.reason,
        )
        if allow_live:
            return RemediationResult(
                action=action,
                status=ActionStatus.success,
                message=f"Executed {self.action_name} on {self.target}",
            )
        return RemediationResult(
            action=action,
            status=ActionStatus.skipped,
            message=(
                f"Dry-run only. Set ALLOW_LIVE_REMEDIATION=true to execute " f"{self.action_name}"
            ),
        )


class RemediationRouter:
    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register(self, metric_name: str, handler: Handler) -> None:
        self._handlers[metric_name] = handler

    def dispatch(self, anomaly: AnomalyEvent, *, allow_live: bool) -> RemediationResult:
        handler = self._handlers.get(anomaly.metric.name)
        if handler is None:
            action = RemediationAction(
                name="no_op",
                target=anomaly.metric.name,
                dry_run=True,
                rationale=f"No remediation handler registered for {anomaly.metric.name}",
            )
            return RemediationResult(
                action=action,
                status=ActionStatus.skipped,
                message="No handler configured",
            )
        return handler.execute(anomaly, allow_live=allow_live)
