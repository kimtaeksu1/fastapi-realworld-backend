# ──────────────────────────────────────────────
# Environment
# ──────────────────────────────────────────────

ve:
	python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt

install_hooks:
	pip install -r requirements-ci.txt; \
	pre-commit install

# ──────────────────────────────────────────────
# Docker
# ──────────────────────────────────────────────

docker_build:
	docker-compose up -d --build

docker_build_postgres:
	docker-compose up -d postgres --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_restart:
	docker-compose stop
	docker-compose up -d

docker_logs:
	docker-compose logs --tail=100 -f

# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────

runserver:
	uvicorn conduit.app:app --host 0.0.0.0

runserver-dev:
	export APP_ENV=dev && uvicorn conduit.app:app --host 0.0.0.0 --reload

# ──────────────────────────────────────────────
# Test
# ──────────────────────────────────────────────

test:
	APP_ENV=test python -m pytest -v ./tests

test-unit:
	APP_ENV=test python -m pytest -v ./tests/services

test-api:
	APP_ENV=test python -m pytest -v ./tests/api

test-cov:
	APP_ENV=test python -m pytest --cov=./conduit --cov-report=term-missing ./tests

# ──────────────────────────────────────────────
# Lint & Format
# ──────────────────────────────────────────────

style:
	flake8 conduit tests

format:
	black conduit tests --check

format-fix:
	black conduit tests
	isort conduit tests

types:
	mypy --namespace-packages -p "conduit" --config-file setup.cfg

types-tests:
	mypy --namespace-packages -p "tests" --config-file setup.cfg

lint:
	flake8 conduit tests
	isort conduit tests --diff
	black conduit tests --check
	mypy --namespace-packages -p "conduit" --config-file setup.cfg

run_hooks:
	pre-commit run --all-files

# ──────────────────────────────────────────────
# Combined: CI / Quality Gate
# ──────────────────────────────────────────────

ci: lint test
	@echo "✅ All checks passed."

check: lint test-cov
	@echo "✅ Lint + coverage passed."

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────

migration:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head

.PHONY: ve install_hooks \
	docker_build docker_build_postgres docker_up docker_down docker_restart docker_logs \
	runserver runserver-dev \
	test test-unit test-api test-cov \
	style format format-fix types types-tests lint run_hooks \
	ci check \
	migration migrate
