## ADDED Requirements

### Requirement: List article comments
The system SHALL return all comments for an article via `GET /api/articles/:slug/comments`. If the requester is authenticated, each comment's author profile SHALL include the correct `following` status.

**Response 200**: `{"comments": [{"id": int, "body": str, "createdAt": datetime, "updatedAt": datetime, "author": {username, bio, image, following}}], "commentsCount": int}`

#### Scenario: Get comments (authenticated)
- **WHEN** an authenticated user requests comments for an existing article
- **THEN** the system returns 200 with comments list, each author's `following` reflects the user's status

#### Scenario: Get comments (unauthenticated)
- **WHEN** an unauthenticated user requests comments for an existing article
- **THEN** the system returns 200 with comments list, all authors have `following: false`

#### Scenario: Get comments for non-existent article
- **WHEN** a user requests comments for an article with a non-existent slug
- **THEN** the system returns 404 with `ArticleNotFoundException`

### Requirement: Create comment
The system SHALL allow authenticated users to add a comment to an article via `POST /api/articles/:slug/comments`. The comment author is set to the current user.

**Request**: `{"comment": {"body": str (min 1)}}`
**Response 200**: `{"comment": {"id": int, "body": str, "createdAt": datetime, "updatedAt": datetime, "author": {username, bio, image, following}}}`

#### Scenario: Successfully create comment
- **WHEN** an authenticated user submits a valid comment on an existing article
- **THEN** the system creates the comment and returns 200 with comment data

#### Scenario: Create comment on non-existent article
- **WHEN** an authenticated user tries to comment on a non-existent article
- **THEN** the system returns 404 with `ArticleNotFoundException`

#### Scenario: Empty comment body
- **WHEN** an authenticated user submits a comment with empty body
- **THEN** the system returns 422 with `RequestValidationError`

#### Scenario: Unauthenticated create comment
- **WHEN** an unauthenticated user tries to create a comment
- **THEN** the system returns 403 error

### Requirement: Delete comment
The system SHALL allow the comment author to delete their comment via `DELETE /api/articles/:slug/comments/:id`. Only the comment author can delete. Returns 204 No Content.

#### Scenario: Author deletes own comment
- **WHEN** the comment author sends a delete request for their comment
- **THEN** the system deletes the comment and returns 204

#### Scenario: Non-author tries to delete comment
- **WHEN** a user who is not the comment author tries to delete it
- **THEN** the system returns 403 with `CommentPermissionException`

#### Scenario: Delete comment on non-existent article
- **WHEN** a user tries to delete a comment on a non-existent article slug
- **THEN** the system returns 404 with `ArticleNotFoundException`

#### Scenario: Delete non-existent comment
- **WHEN** a user tries to delete a comment that does not exist
- **THEN** the system returns 404 with `CommentNotFoundException`
