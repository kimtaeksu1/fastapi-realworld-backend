## ADDED Requirements

### Requirement: Create article
The system SHALL allow authenticated users to create articles via `POST /api/articles`. A slug is auto-generated from the title. Tags are associated with the article upon creation.

**Request**: `{"article": {"title": str (min 5), "description": str (min 10), "body": str (min 10), "tagList": list[str]}}`
**Response 200**: `{"article": {slug, title, description, body, tagList, createdAt, updatedAt, favorited, favoritesCount, author}}`

#### Scenario: Create article with tags
- **WHEN** an authenticated user submits a valid article with tags
- **THEN** the system creates the article, associates tags, and returns 200 with `favorited: false`, `favoritesCount: 0`

#### Scenario: Create article validation failure
- **WHEN** a request has title shorter than 5 chars, or description/body shorter than 10 chars
- **THEN** the system returns 422 with `RequestValidationError`

### Requirement: Get article by slug
The system SHALL return a single article via `GET /api/articles/:slug`. If authenticated, the response includes whether the user has favorited the article and whether they follow the author.

#### Scenario: Get existing article (authenticated)
- **WHEN** an authenticated user requests an article by slug
- **THEN** the system returns 200 with article data, `favorited` and author `following` reflect the user's status

#### Scenario: Get existing article (unauthenticated)
- **WHEN** an unauthenticated user requests an article by slug
- **THEN** the system returns 200 with `favorited: false` and author `following: false`

#### Scenario: Article not found
- **WHEN** a user requests an article with a non-existent slug
- **THEN** the system returns 404 with `ArticleNotFoundException`

### Requirement: Update article
The system SHALL allow the article author to update their article via `PUT /api/articles/:slug`. Only the author can update. All fields are optional (title, description, body).

**Request**: `{"article": {"title?": str, "description?": str, "body?": str}}`

#### Scenario: Author updates own article
- **WHEN** the article author sends a valid update request
- **THEN** the system updates the article and returns 200 with updated data

#### Scenario: Non-author tries to update
- **WHEN** a user who is not the author tries to update an article
- **THEN** the system returns 403 with `ArticlePermissionException`

### Requirement: Delete article
The system SHALL allow the article author to delete their article via `DELETE /api/articles/:slug`. Only the author can delete. Returns 204 No Content on success.

#### Scenario: Author deletes own article
- **WHEN** the article author sends a delete request
- **THEN** the system deletes the article and returns 204

#### Scenario: Non-author tries to delete
- **WHEN** a user who is not the author tries to delete an article
- **THEN** the system returns 403 with `ArticlePermissionException`

### Requirement: Global article feed
The system SHALL return a paginated list of articles via `GET /api/articles` with optional filters. Supports `tag`, `author`, `favorited` query params. Pagination via `limit` (default 20, max 20) and `offset` (default 0).

**Response 200**: `{"articles": [...], "articlesCount": int}`

#### Scenario: Unfiltered global feed
- **WHEN** a user requests `GET /api/articles` without filters
- **THEN** the system returns articles with total count, paginated by defaults

#### Scenario: Filter by tag
- **WHEN** a user requests `GET /api/articles?tag=python`
- **THEN** the system returns only articles tagged with "python"

#### Scenario: Filter by author
- **WHEN** a user requests `GET /api/articles?author=jake`
- **THEN** the system returns only articles by author "jake"

#### Scenario: Filter by favorited
- **WHEN** a user requests `GET /api/articles?favorited=jake`
- **THEN** the system returns only articles favorited by user "jake"

### Requirement: Personal article feed
The system SHALL return articles from followed authors via `GET /api/articles/feed`. Requires authentication. Supports `limit` and `offset` pagination.

#### Scenario: Authenticated user gets feed
- **WHEN** an authenticated user requests their feed
- **THEN** the system returns articles only from authors the user follows, with total count

#### Scenario: Unauthenticated feed request
- **WHEN** an unauthenticated user requests the feed endpoint
- **THEN** the system returns 403 error
