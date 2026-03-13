---
name: fix-issue
description: Fix a GitHub issue using spec context and project conventions. Use when the user says "fix issue", "resolve issue", or references a GitHub issue number.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(APP_ENV=test python -m pytest *), Edit, Write
---

Fix GitHub issue #$ARGUMENTS using OpenSpec specifications as the source of truth.

## Steps

1. **Read the issue**:
   ```bash
   gh issue view $ARGUMENTS
   ```
   Understand the problem, acceptance criteria, and any labels.

2. **Find the relevant spec**:
   - Based on the issue content, identify which capability is affected
   - Read the corresponding spec: `openspec/changes/api-spec-documentation/specs/{capability}/spec.md`
   - Read the tasks file: `openspec/changes/api-spec-documentation/tasks.md`

3. **Locate the code**:
   - Use the capability-to-file mapping:

   | Capability | Key files |
   |---|---|
   | authentication | `conduit/api/routes/authentication.py`, `conduit/services/auth.py` |
   | user-management | `conduit/api/routes/users.py`, `conduit/services/user.py` |
   | profiles | `conduit/api/routes/profile.py`, `conduit/services/profile.py` |
   | articles | `conduit/api/routes/article.py`, `conduit/services/article.py` |
   | comments | `conduit/api/routes/comment.py`, `conduit/services/comment.py` |
   | favorites | `conduit/api/routes/article.py`, `conduit/services/article.py` |
   | tags | `conduit/api/routes/tag.py`, `conduit/services/tag.py` |
   | infrastructure | `conduit/api/middlewares.py`, `conduit/core/container.py`, `conduit/core/dependencies.py` |

   - Read the relevant source files to understand current behavior

4. **Implement the fix**:
   - Follow the layered architecture: changes flow ORM -> Repo -> Service -> API
   - Ensure the fix aligns with the spec's requirements and scenarios
   - Add or update exception classes in `conduit/core/exceptions.py` if needed

5. **Write or update tests**:
   - Check existing tests in `tests/api/routes/`
   - Add test cases that cover the fix, following the spec's WHEN/THEN scenarios
   - Use project fixtures: `test_client`, `authorized_test_client`, `test_user`, `test_article`

6. **Verify**:
   ```bash
   APP_ENV=test python -m pytest -v ./tests/api/routes/ -x
   make lint
   ```

7. **Summarize** what was changed and which spec requirements are now satisfied.
   Reference the issue number in the summary: `Fixes #$ARGUMENTS`.
