## ADDED Requirements

### Requirement: Favorite article
The system SHALL allow authenticated users to favorite an article via `POST /api/articles/:slug/favorite`. The system SHALL prevent duplicate favorites. On success, the `favoritesCount` is incremented and `favorited` is set to true.

**Response 200**: `{"article": {slug, title, description, body, tagList, createdAt, updatedAt, favorited: true, favoritesCount: int, author}}`

#### Scenario: Successfully favorite an article
- **WHEN** an authenticated user favorites an article they have not yet favorited
- **THEN** the system creates the favorite, returns 200 with `favorited: true` and incremented `favoritesCount`

#### Scenario: Favorite already-favorited article
- **WHEN** an authenticated user tries to favorite an article they already favorited
- **THEN** the system returns 400 with `ArticleAlreadyFavoritedException`

#### Scenario: Favorite non-existent article
- **WHEN** an authenticated user tries to favorite an article with a non-existent slug
- **THEN** the system returns 404 with `ArticleNotFoundException`

#### Scenario: Unauthenticated favorite
- **WHEN** an unauthenticated user tries to favorite an article
- **THEN** the system returns 403 error

### Requirement: Unfavorite article
The system SHALL allow authenticated users to unfavorite an article via `DELETE /api/articles/:slug/favorite`. The system SHALL verify the article is currently favorited. On success, the `favoritesCount` is decremented and `favorited` is set to false.

**Response 200**: `{"article": {slug, title, description, body, tagList, createdAt, updatedAt, favorited: false, favoritesCount: int, author}}`

#### Scenario: Successfully unfavorite an article
- **WHEN** an authenticated user unfavorites an article they currently have favorited
- **THEN** the system removes the favorite, returns 200 with `favorited: false` and decremented `favoritesCount`

#### Scenario: Unfavorite not-favorited article
- **WHEN** an authenticated user tries to unfavorite an article they have not favorited
- **THEN** the system returns 400 with `ArticleNotFavoritedException`

#### Scenario: Unfavorite non-existent article
- **WHEN** an authenticated user tries to unfavorite an article with a non-existent slug
- **THEN** the system returns 404 with `ArticleNotFoundException`
