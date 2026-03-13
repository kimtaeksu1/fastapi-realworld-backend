## ADDED Requirements

### Requirement: DI container wiring
The system SHALL use a `Container` class to wire repositories into services. The container creates async database sessions via `async_sessionmaker`. Services are resolved through `@lru_cache` provider functions in `providers.py`, injected as FastAPI `Depends()` via `Annotated` type aliases in `dependencies.py`.

#### Scenario: Service resolution chain
- **WHEN** a route handler declares a service dependency (e.g., `IArticleService`)
- **THEN** FastAPI resolves it through providers -> container -> concrete service with all repository dependencies injected

#### Scenario: Singleton provider caching
- **WHEN** multiple requests resolve the same service provider
- **THEN** the `@lru_cache` decorator returns the same container/service instance

### Requirement: Async session management
The system SHALL manage database sessions as async context managers with auto-commit on success and auto-rollback on exception. Sessions are yielded via `Container.session()` and injected as `DBSession` dependency.

#### Scenario: Successful request commits
- **WHEN** a request completes without exception
- **THEN** the session is committed and closed

#### Scenario: Exception triggers rollback
- **WHEN** a request raises an exception during processing
- **THEN** the session is rolled back and closed before the exception propagates

### Requirement: Rate limiting middleware
The system SHALL enforce rate limiting via `RateLimitingMiddleware` with a limit of 100 requests per IP per 1-minute sliding window. Rate limit state is stored in-memory per process.

#### Scenario: Within rate limit
- **WHEN** a client sends fewer than 100 requests within 1 minute
- **THEN** all requests are processed normally

#### Scenario: Rate limit exceeded
- **WHEN** a client exceeds 100 requests within 1 minute
- **THEN** the system returns 429 with `RateLimitExceededException`

#### Scenario: Rate limit window reset
- **WHEN** more than 1 minute has elapsed since the last request from an IP
- **THEN** the request counter resets to 1

### Requirement: Error response format
The system SHALL return all errors in a consistent JSON format: `{"status": "error", "status_code": int, "type": str, "message": str, "errors": dict}`. This covers internal exceptions, validation errors, and HTTP exceptions.

#### Scenario: Internal exception format
- **WHEN** a `BaseInternalException` subclass is raised
- **THEN** the response includes `status`, `status_code`, `type` (class name), `message`, and `errors` fields

#### Scenario: Validation error format
- **WHEN** Pydantic validation fails on a request
- **THEN** the system returns 422 with `type: "RequestValidationError"` and formatted field errors

### Requirement: JWT security scheme
The system SHALL use a custom `HTTPTokenHeader` that extracts JWT from `Authorization: Token xxx.yyy.zzz` header. Two variants exist: `token_security` (raises on missing) and `token_security_optional` (returns None on missing).

#### Scenario: Required auth on protected endpoint
- **WHEN** a protected endpoint is accessed without Authorization header
- **THEN** `token_security` raises a 403 error

#### Scenario: Optional auth returns None
- **WHEN** an optional-auth endpoint is accessed without Authorization header
- **THEN** `token_security_optional` returns None and the request proceeds with `current_user=None`

### Requirement: Pagination defaults
The system SHALL provide default pagination for article list endpoints with `limit=20` (max 20, min 1) and `offset=0` (min 0). If the client requests `limit > 20`, the system caps it at 20.

#### Scenario: Default pagination
- **WHEN** a client requests articles without pagination params
- **THEN** the system uses `limit=20, offset=0`

#### Scenario: Limit capped at maximum
- **WHEN** a client requests `limit=50`
- **THEN** the system caps the limit to 20
