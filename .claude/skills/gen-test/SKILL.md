---
name: gen-test
description: Generate pytest API tests from OpenSpec spec files. Use when writing tests for endpoints, or when the user says "generate tests", "write tests", or "test this spec".
argument-hint: "[capability-name] (e.g., authentication, articles, comments)"
---

Generate pytest API tests from OpenSpec specifications for this FastAPI RealWorld (Conduit) backend.

**Input**: `$ARGUMENTS` is a capability name (e.g., `authentication`, `articles`, `comments`, `favorites`, `profiles`, `tags`, `user-management`, `infrastructure`).

## Steps

1. **Read the spec file**:
   - Read `openspec/changes/api-spec-documentation/specs/$ARGUMENTS/spec.md`
   - If `$ARGUMENTS` is empty, ask the user which capability to generate tests for

2. **Read existing test patterns** for reference:
   - Read `tests/conftest.py` for available fixtures (`test_client`, `authorized_test_client`, `test_user`, `test_article`, `jwt_token`, `session`)
   - Read `tests/utils.py` for helper functions
   - Check `tests/api/routes/` for existing test files to avoid duplication

3. **Generate one test function per scenario** in the spec:
   - Each `#### Scenario:` block becomes a `async def test_...()` function
   - Map **WHEN** to test setup/action, **THEN** to assertions
   - Use `@pytest.mark.anyio` decorator on all async tests
   - Use `httpx.AsyncClient` fixtures (`test_client` for unauthenticated, `authorized_test_client` for authenticated)

4. **Follow project test conventions**:
   - File naming: `test_{capability}.py` under `tests/api/routes/`
   - Import response schemas for type-safe assertions: `from conduit.api.schemas.responses.{module} import {Response}`
   - Assert HTTP status codes explicitly: `assert response.status_code == 200`
   - Assert error response structure: `{"status": "error", "status_code": int, "type": str, "message": str}`
   - Use `test_user`, `test_article` fixtures for pre-created entities
   - Create additional test data via `tests/utils.py` helpers when needed

5. **Test file structure**:
   ```python
   import pytest
   from httpx import AsyncClient
   # ... imports

   # --- Requirement: {requirement name} ---

   @pytest.mark.anyio
   async def test_{scenario_snake_case}(...) -> None:
       # WHEN: {action from spec}
       response = await client.{method}(url="...", json=payload)
       # THEN: {assertion from spec}
       assert response.status_code == {expected}
   ```

6. **Write the test file** and run it:
   ```bash
   APP_ENV=test python -m pytest -v ./tests/api/routes/test_{name}.py
   ```

## Endpoint-to-URL mapping

| Spec endpoint | Test URL |
|--------------|----------|
| `POST /api/users` | `/users` |
| `POST /api/users/login` | `/users/login` |
| `GET /api/user` | `/user` |
| `PUT /api/user` | `/user` |
| `GET /api/profiles/:username` | `/profiles/{username}` |
| `POST /api/profiles/:username/follow` | `/profiles/{username}/follow` |
| `DELETE /api/profiles/:username/follow` | `/profiles/{username}/follow` |
| `GET /api/articles` | `/articles` |
| `GET /api/articles/feed` | `/articles/feed` |
| `GET /api/articles/:slug` | `/articles/{slug}` |
| `POST /api/articles` | `/articles` |
| `PUT /api/articles/:slug` | `/articles/{slug}` |
| `DELETE /api/articles/:slug` | `/articles/{slug}` |
| `POST /api/articles/:slug/favorite` | `/articles/{slug}/favorite` |
| `DELETE /api/articles/:slug/favorite` | `/articles/{slug}/favorite` |
| `GET /api/articles/:slug/comments` | `/articles/{slug}/comments` |
| `POST /api/articles/:slug/comments` | `/articles/{slug}/comments` |
| `DELETE /api/articles/:slug/comments/:id` | `/articles/{slug}/comments/{id}` |
| `GET /api/tags` | `/tags` |
