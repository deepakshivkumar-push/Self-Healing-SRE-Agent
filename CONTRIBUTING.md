# Contributing

## Development workflow

1. Copy `.env.example` to `.env` and adjust values.
2. Install dependencies:
   ```bash
   make setup
   ```
3. Run checks before opening a PR:
   ```bash
   make lint
   make typecheck
   make test
   ```
4. Run demo locally:
   ```bash
   make demo
   ```

## PR expectations

- Keep remediation safe by default (`ALLOW_LIVE_REMEDIATION=false`).
- Add or update tests for behavior changes.
- Keep CI green (lint, typecheck, tests, docker build).
