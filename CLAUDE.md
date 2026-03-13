# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend implementing the [RealWorld](https://github.com/gothinkster/realworld) API spec (Conduit). Python 3.12, PostgreSQL (async via asyncpg), SQLAlchemy 2.0, Pydantic 2.

## Commands

```bash
# Setup
make ve                          # Create venv + install deps
make docker_build_postgres       # Start PostgreSQL only
make migrate                     # Run alembic migrations

# Run
make runserver                   # uvicorn on 0.0.0.0:8000
make runserver-dev               # uvicorn with --reload (sets APP_ENV=dev)

# Test (requires .env.test with separate POSTGRES_DB)
make test                        # All tests (services + api)
make test-unit                   # Service unit tests only
make test-api                    # API route tests only
make test-cov                    # All tests with coverage report
APP_ENV=test python -m pytest -v ./tests/api/routes/test_article.py       # single file
APP_ENV=test python -m pytest -v ./tests/api/routes/test_article.py -k "test_name"  # single test

# Lint & Format
make lint                        # flake8 + isort + black + mypy (conduit + tests)
make style                       # flake8 only
make format                      # black --check only
make format-fix                  # black + isort auto-fix
make types                       # mypy only
make run_hooks                   # pre-commit run --all-files

# Combined
make ci                          # lint + test (CI pipeline)
make check                       # lint + test-cov (with coverage)

# Migrations
make migration message="description"   # autogenerate new migration
make migrate                           # alembic upgrade head
```

## Architecture

Layered architecture with strict dependency direction: **API -> Services -> Repositories -> ORM**.

```
conduit/
  api/
    router.py        # Central route registration (includes all sub-routers)
    routes/          # FastAPI route handlers (async)
    schemas/
      requests/      # Pydantic request models
      responses/     # Pydantic response models
    middlewares.py   # RateLimitingMiddleware
  services/          # Business logic (async). Depend on repositories via interfaces.
  interfaces/
    repositories/    # ABC for each repository
    services/        # ABC for each service
  dtos/
    domain/          # Business DTOs (UserDTO, ArticleDTO, etc.) - used by services & API
    records/         # Persistence DTOs (ArticleRecordDTO, etc.) - returned by repositories
  infrastructure/
    models.py        # SQLAlchemy ORM models (User, Article, Tag, Comment, Favorite, Follower, ArticleTag)
    repositories/    # Concrete repository implementations
    alembic/         # Migration versions
  core/
    container.py     # DI container - wires repos into services
    providers.py     # @lru_cache provider functions for FastAPI Depends()
    dependencies.py  # Annotated type aliases (DBSession, CurrentUser, JWTToken, etc.)
    security.py      # HTTPTokenHeader - custom "Token xxx.yyy.zzz" auth scheme
    config.py        # get_app_settings() loads env-specific settings
    settings/        # base, app, development, production, test
    exceptions.py    # Global exception handlers
    logging.py       # structlog-based logging configuration
    utils/           # Helpers: date.py, errors.py, slug.py
```

### Key Patterns

- **DI flow**: `Container` (creates repos/services) -> `providers.py` (`@lru_cache` singletons) -> `dependencies.py` (`Annotated[Service, Depends(...)]`) -> route handlers.
- **DTO split**: `dtos/domain/` for business logic, `dtos/records/` for persistence. Services convert between them. DTOs use `@classmethod` factory methods (e.g., `from_record()`, `from_model()`).
- **Auth**: JWT with `Authorization: Token {jwt}` header (not Bearer). `CurrentUser` dependency for required auth, `CurrentOptionalUser` for optional.
- **Session management**: `Container.context_session()` is an async context manager yielding `AsyncSession` with auto-commit/rollback. Injected via `DBSession` dependency.
- **All DB operations are async** — routes, services, and repositories all use `async/await`.

### Testing

- Tests use a real PostgreSQL database (configured via `.env.test`).
- `conftest.py` fixtures: `create_test_db` (session-scoped, creates/drops DB), `create_tables` (function-scoped, autouse, creates/drops tables per test), `test_client` (httpx `AsyncClient`), `authorized_test_client` (with JWT auth header).
- Async test support: `anyio_backend` fixture returns `"asyncio"`.
- Key fixtures: `test_user`, `test_article`, `jwt_token`, `not_exists_user`, `not_exists_jwt_token` provide pre-created entities and tokens.

## Code Style

- **Black**: 88 chars, py312 target, skip magic trailing comma
- **isort**: profile compatible with black (multi_line_output=3, trailing comma)
- **Flake8**: max-complexity 15, cognitive-complexity 15
- **MyPy**: strict mode (`disallow_untyped_defs`, `strict_optional`)
- Pre-commit hooks enforce all of the above plus pyupgrade (py312+) and unit tests

## Terminal Output Style

When displaying information about **plugin commands**, **skills**, or **sub-agents** in terminal output, use **green (ANSI escape)** to make them visually distinct:
- Skill invocations: `\033[32m/gen-test articles\033[0m`
- Sub-agent launches: `\033[32m[Agent: executor]\033[0m`
- Plugin/MCP tool calls: `\033[32m[MCP: lsp_hover]\033[0m`

This ensures users can immediately distinguish AI orchestration actions from regular code output in the terminal.
