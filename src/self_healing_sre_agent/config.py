from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    service_name: str = "self-healing-sre-agent"
    log_level: str = "INFO"
    demo_mode: bool = True
    polling_interval_seconds: float = 1.0
    anomaly_window_size: int = 20
    anomaly_min_samples: int = 8
    anomaly_zscore_threshold: float = 2.5
    anomaly_std_epsilon: float = 0.001
    max_iterations: int = 0
    allow_live_remediation: bool = False


def _as_bool(raw: str | None, default: bool) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _load_env_file(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def load_settings(env_file: str | os.PathLike[str] = ".env") -> Settings:
    defaults = Settings()
    env_path = Path(env_file)
    if env_path.exists():
        _load_env_file(env_path)

    return Settings(
        service_name=os.getenv("SERVICE_NAME", defaults.service_name),
        log_level=os.getenv("LOG_LEVEL", defaults.log_level),
        demo_mode=_as_bool(os.getenv("DEMO_MODE"), defaults.demo_mode),
        polling_interval_seconds=float(
            os.getenv("POLLING_INTERVAL_SECONDS", defaults.polling_interval_seconds)
        ),
        anomaly_window_size=int(os.getenv("ANOMALY_WINDOW_SIZE", defaults.anomaly_window_size)),
        anomaly_min_samples=int(os.getenv("ANOMALY_MIN_SAMPLES", defaults.anomaly_min_samples)),
        anomaly_zscore_threshold=float(
            os.getenv("ANOMALY_ZSCORE_THRESHOLD", defaults.anomaly_zscore_threshold)
        ),
        anomaly_std_epsilon=float(os.getenv("ANOMALY_STD_EPSILON", defaults.anomaly_std_epsilon)),
        max_iterations=int(os.getenv("MAX_ITERATIONS", defaults.max_iterations)),
        allow_live_remediation=_as_bool(
            os.getenv("ALLOW_LIVE_REMEDIATION"), defaults.allow_live_remediation
        ),
    )
