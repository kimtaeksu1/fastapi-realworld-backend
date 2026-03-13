---
name: explain-layer
description: Trace the full request flow for a feature through all architecture layers. Use when the user says "explain", "trace", "how does X work", or wants to understand the codebase.
argument-hint: "[feature-or-endpoint] (e.g., 'create article', 'POST /articles', 'login')"
context: fork
agent: Explore
---

Trace the full request lifecycle for `$ARGUMENTS` through every architecture layer of this FastAPI RealWorld backend.

## Steps

1. **Identify the endpoint** from user input. Map common terms:
   - "login" -> `POST /api/users/login`
   - "register" / "signup" -> `POST /api/users`
   - "create article" -> `POST /api/articles`
   - "feed" -> `GET /api/articles/feed`
   - "follow" -> `POST /api/profiles/:username/follow`
   - "favorite" -> `POST /api/articles/:slug/favorite`

2. **Read the spec** for business context:
   - `openspec/changes/api-spec-documentation/specs/{capability}/spec.md`

3. **Trace through each layer** (in request order):

### Layer 1: Route Registration
- File: `conduit/api/router.py`
- Show how the route is registered with prefix and tags

### Layer 2: Dependency Injection
- File: `conduit/core/dependencies.py`
- Show the `Annotated` type aliases used in the route signature
- File: `conduit/core/providers.py` -> `conduit/core/container.py`
- Show how services and repos are wired together

### Layer 3: Request Validation
- File: `conduit/api/schemas/requests/{module}.py`
- Show Pydantic model fields, validation rules, `to_dto()` conversion

### Layer 4: Authentication (if applicable)
- File: `conduit/core/security.py` -> `conduit/core/dependencies.py`
- Show `HTTPTokenHeader` -> `get_current_user()` chain
- Explain `CurrentUser` (required) vs `CurrentOptionalUser` (optional)

### Layer 5: Route Handler
- File: `conduit/api/routes/{module}.py`
- Show the async handler function and how it calls the service

### Layer 6: Service (Business Logic)
- File: `conduit/services/{module}.py`
- Show permission checks, business rules, exception handling
- Show DTO conversions (domain <-> record)

### Layer 7: Repository (Data Access)
- File: `conduit/infrastructure/repositories/{module}.py`
- Show SQLAlchemy async queries

### Layer 8: Response Serialization
- File: `conduit/api/schemas/responses/{module}.py`
- Show `from_dto()` conversion and JSON field aliases

### Layer 9: Error Handling (if applicable)
- File: `conduit/core/exceptions.py`
- Show which exceptions can be raised and their status codes/messages

4. **Output format** — present as a numbered flow:

```
Request: POST /api/articles
Authorization: Token xxx.yyy.zzz

1. [Router]      router.py:24 — prefix="/articles", tags=["Articles"]
2. [Auth]        dependencies.py:86 — get_current_user() extracts JWT -> UserDTO
3. [Validation]  requests/article.py:41 — CreateArticleRequest validates body
4. [Handler]     routes/article.py:80 — create_article() calls service
5. [Service]     services/article.py:42 — create_new_article() adds to repo, links tags
6. [Repository]  repositories/article.py — ArticleRepository.add() INSERT into articles
7. [Response]    responses/article.py:37 — ArticleResponse.from_dto() serializes
8. [Errors]      exceptions.py:89 — ArticleCreateException (500) on DB failure

Flow: Client -> Auth -> Validate -> Route -> Service -> Repo -> DB -> Response
```

5. **Highlight key design decisions** relevant to this endpoint from the spec.
