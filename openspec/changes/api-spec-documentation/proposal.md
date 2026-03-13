## Why

This FastAPI RealWorld (Conduit) backend lacks formal API specification documents. Without specs, AI-assisted development (vibe coding) has no single source of truth for generating tests, validating implementations, or planning migrations. Documenting the existing API surface as OpenSpec artifacts enables automated test generation, CI/CD pipeline design, and reliable AI collaboration.

## What Changes

- Create specification documents for all 7 capability areas of the existing API
- Each spec captures endpoints, request/response schemas, business rules, and error cases
- No code changes — this is a documentation-only change that captures the current behavior as-is

## Capabilities

### New Capabilities

- `authentication`: User registration (`POST /users`) and login (`POST /users/login`) with JWT token issuance
- `user-management`: Get current user (`GET /user`), update current user (`PUT /user`) with JWT auth
- `profiles`: View user profiles (`GET /profiles/:username`), follow/unfollow users
- `articles`: Full CRUD for articles, global feed with filters, personal feed from followed authors, slug-based addressing
- `comments`: Create/list/delete comments on articles
- `favorites`: Favorite/unfavorite articles (`POST/DELETE /articles/:slug/favorite`)
- `tags`: List all available tags (`GET /tags`)
- `infrastructure`: DI container, async DB sessions, rate limiting middleware, JWT security, settings management

### Modified Capabilities

(none — no existing specs)

## Impact

- **New files**: 8 spec files under `openspec/changes/api-spec-documentation/specs/`
- **No code changes**: Existing application code is unaffected
- **Downstream use**: Specs become the source of truth for test generation (Epic 2), CI/CD pipeline design (Epic 3), and migration planning (Epic 4)
