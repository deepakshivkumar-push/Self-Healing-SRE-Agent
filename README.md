# Self-Healing SRE Agent

Production-ready Python service that ingests metrics, detects anomalies in near real-time, and routes safe remediation actions.

## Architecture

- **Ingestion**: pluggable metric stream provider (`ingestion.py`, synthetic demo included)
- **Detection**: z-score baseline detector with rolling windows (`detector.py`)
- **Remediation**: extensible handler router with safe mock defaults (`remediation.py`)
- **Configuration**: environment-driven settings with `.env` support (`config.py`)
- **Entrypoint**: CLI service (`sre-agent`)

Project layout:

```text
src/self_healing_sre_agent/
  cli.py
  config.py
  detector.py
  ingestion.py
  models.py
  remediation.py
  service.py
tests/
.github/workflows/
```

## Quickstart (local)

```bash
cp .env.example .env
make setup
make demo
```

Run continuously:

```bash
make run
```

## Docker

```bash
docker build -t self-healing-sre-agent:local .
docker run --rm --env-file .env self-healing-sre-agent:local
```

With compose:

```bash
docker compose up --build
```

## Configuration

Use `.env` (see `.env.example`):

- `POLLING_INTERVAL_SECONDS`: loop interval
- `ANOMALY_WINDOW_SIZE`, `ANOMALY_MIN_SAMPLES`, `ANOMALY_ZSCORE_THRESHOLD`: detector tuning
- `MAX_ITERATIONS`: demo bounded run (`0` means infinite)
- `ALLOW_LIVE_REMEDIATION`: safety gate for non-dry-run execution

## CI/CD

- **CI** (`.github/workflows/ci.yml`): lint, format check, mypy, pytest, Docker build validation on PRs/pushes to `main`
- **CD** (`.github/workflows/cd.yml`): builds and pushes image to GHCR on version tags (`v*`) or manual dispatch, plus deploy job scaffold

GHCR uses `GITHUB_TOKEN` with `packages: write` permission.

## Remediation safety

By default, remediation is **dry-run only**. Set `ALLOW_LIVE_REMEDIATION=true` only after integrating and reviewing real handlers.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
