PYTHON ?= python3

.PHONY: setup lint format typecheck test run demo docker-build docker-run compose-up compose-down

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

typecheck:
	mypy src

test:
	pytest

run:
	sre-agent

demo:
	sre-agent --iterations 30

docker-build:
	docker build -t self-healing-sre-agent:local .

docker-run:
	docker run --rm --env-file .env self-healing-sre-agent:local

compose-up:
	docker compose up --build

compose-down:
	docker compose down
