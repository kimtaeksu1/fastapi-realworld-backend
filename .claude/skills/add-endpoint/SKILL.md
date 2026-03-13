---
name: add-endpoint
description: Scaffold a new API endpoint across all architecture layers. Use when the user says "add endpoint", "create endpoint", "new route", or "new API".
argument-hint: "[method] [path] [description] (e.g., GET /api/articles/:slug/stats 'Get article statistics')"
---

Scaffold a new API endpoint for this FastAPI RealWorld (Conduit) backend following the layered architecture.

**Input**: `$ARGUMENTS` describes the endpoint (HTTP method, path, brief description).

## Architecture reference

Read `openspec/changes/api-spec-documentation/design.md` for architectural decisions.
Read `openspec/changes/api-spec-documentation/specs/infrastructure/spec.md` for DI and session patterns.

## Steps

Create or modify files in this exact order (dependency direction: ORM -> Repository -> Service -> API):

### 1. ORM Model (if new table needed)
- File: `conduit/infrastructure/models.py`
- Add SQLAlchemy model class inheriting from `Base`
- Add `created_at`, `updated_at` timestamp columns

### 2. DTOs
- **Records DTO** (persistence layer): `conduit/dtos/records/{entity}.py`
  - Dataclass with fields matching DB columns
  - Used by repositories only
- **Domain DTO** (business layer): `conduit/dtos/domain/{entity}.py`
  - Dataclass with business-level fields
  - Include `@classmethod from_record()` factory method
  - Used by services and API layer

### 3. Repository Interface + Implementation
- **Interface**: `conduit/interfaces/repositories/{entity}.py`
  - ABC with async method signatures
  - Methods accept/return record DTOs
- **Implementation**: `conduit/infrastructure/repositories/{entity}.py`
  - Concrete class implementing the interface
  - Use `AsyncSession` for all DB operations
  - Use SQLAlchemy 2.0 `select()` style queries

### 4. Service Interface + Implementation
- **Interface**: `conduit/interfaces/services/{entity}.py`
  - ABC with async method signatures
  - Methods accept/return domain DTOs
- **Implementation**: `conduit/services/{entity}.py`
  - Inject repository interfaces via `__init__`
  - Convert between record DTOs and domain DTOs
  - Raise domain exceptions from `conduit/core/exceptions.py`

### 5. Request/Response Schemas
- **Request**: `conduit/api/schemas/requests/{entity}.py`
  - Pydantic `BaseModel` with validation (`Field(min_length=...)`)
  - Nested wrapper (e.g., `{"article": {...}}` pattern)
  - Include `to_dto()` method
- **Response**: `conduit/api/schemas/responses/{entity}.py`
  - Pydantic `BaseModel` with `@classmethod from_dto()`
  - Use `Field(alias="camelCase")` for JSON output

### 6. DI Wiring
- Add repository factory to `conduit/core/container.py`
- Add service factory to `conduit/core/container.py`
- Add `@lru_cache` provider to `conduit/core/providers.py`
- Add `Annotated` type alias to `conduit/core/dependencies.py`

### 7. Route Handler
- File: `conduit/api/routes/{entity}.py`
- Use `APIRouter()`
- Inject dependencies via `Annotated` types (`DBSession`, `CurrentUser`, service)
- Return response schema instances
- Register in `conduit/api/router.py`

### 8. Exception (if needed)
- Add to `conduit/core/exceptions.py`
- Extend `BaseInternalException` with `_status_code` and `_message`

### 9. Migration (if new table)
```bash
make migration message="add {entity} table"
```

### 10. Verification
- Run `make lint` to verify code style
- Run `make types` to verify type checking
- Create a basic test following `gen-test` skill patterns
