---
name: check-spec
description: Verify code changes comply with OpenSpec specifications. Use when reviewing changes, after refactoring, or when the user says "check spec", "verify spec", or "spec compliance".
argument-hint: "[capability-name or file-path] (e.g., articles, conduit/services/article.py)"
---

Verify that the current implementation matches the OpenSpec specifications for this project.

**Input**: `$ARGUMENTS` is either a capability name or a file path to check.

## Steps

1. **Determine scope**:
   - If `$ARGUMENTS` is a capability name (e.g., `articles`): check all code related to that capability
   - If `$ARGUMENTS` is a file path: determine which capability it belongs to and check that spec
   - If `$ARGUMENTS` is empty: check all capabilities against recent git changes (`git diff --name-only HEAD~1`)

2. **Load the relevant spec**:
   - Read `openspec/changes/api-spec-documentation/specs/{capability}/spec.md`
   - Extract all `### Requirement:` blocks and their `#### Scenario:` blocks

3. **Map spec to code** — for each requirement, verify:

   | Spec element | Code location to check |
   |---|---|
   | Endpoint method + path | `conduit/api/routes/{module}.py` |
   | Request schema validation | `conduit/api/schemas/requests/{module}.py` |
   | Response schema fields | `conduit/api/schemas/responses/{module}.py` |
   | Business rules | `conduit/services/{module}.py` |
   | Error cases + status codes | `conduit/core/exceptions.py` |
   | Auth requirements | Route handler signature (`CurrentUser` vs `CurrentOptionalUser`) |

4. **Check each scenario** against the implementation:
   - **WHEN** condition: Is this code path reachable?
   - **THEN** outcome: Does the code produce the expected result?
   - Focus on: status codes, exception types, field presence, validation rules

5. **Report findings** in this format:

   ```
   ## Spec Compliance Report: {capability}

   ### Passed
   - [x] Requirement: {name} — Scenario: {name} — OK

   ### Issues Found
   - [ ] Requirement: {name} — Scenario: {name}
     - Expected: {what the spec says}
     - Actual: {what the code does}
     - File: {path}:{line}

   ### Not Testable (requires runtime)
   - [ ] Requirement: {name} — Scenario: {name} — Needs integration test
   ```

6. **Suggest fixes** for any issues found, referencing the spec requirement.

## Capability-to-file mapping

| Capability | Route | Service | Exceptions |
|---|---|---|---|
| authentication | routes/authentication.py | services/auth.py | IncorrectLoginInputException, EmailAlreadyTakenException, UserNameAlreadyTakenException |
| user-management | routes/users.py | services/user.py | EmailAlreadyTakenException, UserNameAlreadyTakenException |
| profiles | routes/profile.py | services/profile.py | ProfileNotFoundException, OwnProfileFollowingException, ProfileAlreadyFollowedException |
| articles | routes/article.py | services/article.py | ArticleNotFoundException, ArticlePermissionException, ArticleCreateException |
| comments | routes/comment.py | services/comment.py | CommentNotFoundException, CommentPermissionException, CommentCreateException |
| favorites | routes/article.py | services/article.py | ArticleAlreadyFavoritedException, ArticleNotFavoritedException |
| tags | routes/tag.py | services/tag.py | (none) |
| infrastructure | middlewares.py, dependencies.py | container.py | RateLimitExceededException, IncorrectJWTTokenException |
