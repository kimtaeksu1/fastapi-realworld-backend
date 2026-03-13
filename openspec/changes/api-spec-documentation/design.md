## Context

This is a FastAPI RealWorld (Conduit) backend with a layered architecture: API routes -> Services -> Repositories -> ORM. The codebase uses async PostgreSQL (asyncpg/SQLAlchemy 2.0), Pydantic 2 for validation, and a custom DI container. The project currently lacks formal specification documents, making AI-assisted development unreliable.

## Goals / Non-Goals

**Goals:**
- Document all existing API endpoints, schemas, business rules, and error cases as OpenSpec artifacts
- Each spec file stays under 200 lines for easy reference by Claude skills
- Specs accurately reflect current implementation behavior (not aspirational)
- Specs serve as source of truth for test generation, CI/CD design, and migration planning

**Non-Goals:**
- No code changes — this is documentation only
- No new features or API modifications
- No performance or security recommendations (those belong in separate changes)
- No OpenAPI/Swagger generation — specs are human/AI-readable markdown

## Decisions

### 1. Spec granularity: one file per capability domain
**Decision**: 8 spec files matching the proposal capabilities (authentication, user-management, profiles, articles, comments, favorites, tags, infrastructure).
**Rationale**: Maps 1:1 to route files and service boundaries. Each file stays focused and under 200 lines. Alternative (single monolithic spec) would exceed size limits and be harder to reference.

### 2. Favorites as separate spec from articles
**Decision**: Extract favorites into its own spec despite sharing the `/articles` route prefix.
**Rationale**: Favorites have distinct business rules (idempotency checks, count management) and error cases. Keeping them separate makes each spec more focused and easier to test independently.

### 3. Infrastructure as a spec
**Decision**: Include infrastructure components (DI, sessions, middleware, auth scheme, settings) as a specification.
**Rationale**: These cross-cutting concerns have testable requirements (rate limiting thresholds, session commit/rollback behavior, JWT validation). Without documenting them, test coverage would miss critical system behaviors.

### 4. Scenario-based format for testability
**Decision**: Every requirement includes WHEN/THEN scenarios that map directly to test cases.
**Rationale**: The primary consumer of these specs is test generation. Each scenario becomes a test function. Alternative (prose-only requirements) would require interpretation during test creation.

## Risks / Trade-offs

- **[Spec drift]** Specs may diverge from code as the project evolves. **Mitigation**: Specs are versioned alongside code in openspec/; changes trigger spec updates via the OpenSpec workflow.
- **[Incomplete coverage]** Some edge cases in repository implementations may not be captured. **Mitigation**: Specs focus on service-level behavior visible through the API; internal repository details are implementation concerns.
- **[200-line constraint]** Complex capabilities (articles) may need careful scoping to stay under limit. **Mitigation**: Separate favorites from articles; keep scenarios concise with WHEN/THEN format.
