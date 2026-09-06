from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


@dataclass(slots=True)
class MetricEvent:
    name: str
    value: float
    unit: str
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnomalyEvent:
    metric: MetricEvent
    score: float
    threshold: float
    severity: Severity
    reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class ActionStatus(StrEnum):
    success = "success"
    skipped = "skipped"
    failed = "failed"


@dataclass(slots=True)
class RemediationAction:
    name: str
    target: str
    dry_run: bool
    rationale: str


@dataclass(slots=True)
class RemediationResult:
    action: RemediationAction
    status: ActionStatus
    message: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
