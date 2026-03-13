## 1. Authentication & User Management Tests

- [ ] 1.1 Write unit tests for user registration (success, duplicate email, duplicate username, validation errors)
- [ ] 1.2 Write unit tests for user login (success, wrong email, wrong password)
- [ ] 1.3 Write unit tests for JWT token generation and validation (valid token, expired token, invalid token, missing token)
- [ ] 1.4 Write unit tests for get current user (authenticated, unauthenticated)
- [ ] 1.5 Write unit tests for update current user (update fields, duplicate email/username, empty string handling)

## 2. Profiles & Follow Tests

- [ ] 2.1 Write unit tests for get profile (authenticated with follow status, unauthenticated, not found)
- [ ] 2.2 Write unit tests for follow user (success, follow self, already followed, non-existent user)
- [ ] 2.3 Write unit tests for unfollow user (success, unfollow self, not followed)

## 3. Articles Tests

- [ ] 3.1 Write unit tests for create article (success with tags, validation errors)
- [ ] 3.2 Write unit tests for get article by slug (authenticated, unauthenticated, not found)
- [ ] 3.3 Write unit tests for update article (author success, non-author forbidden)
- [ ] 3.4 Write unit tests for delete article (author success, non-author forbidden)
- [ ] 3.5 Write unit tests for global feed (unfiltered, filter by tag, filter by author, filter by favorited, pagination)
- [ ] 3.6 Write unit tests for personal feed (authenticated with followed authors, unauthenticated rejected)

## 4. Comments Tests

- [ ] 4.1 Write unit tests for list comments (authenticated, unauthenticated, non-existent article)
- [ ] 4.2 Write unit tests for create comment (success, non-existent article, empty body, unauthenticated)
- [ ] 4.3 Write unit tests for delete comment (author success, non-author forbidden, non-existent article/comment)

## 5. Favorites Tests

- [ ] 5.1 Write unit tests for favorite article (success, already favorited, non-existent article, unauthenticated)
- [ ] 5.2 Write unit tests for unfavorite article (success, not favorited, non-existent article)

## 6. Tags Tests

- [ ] 6.1 Write unit tests for list all tags (with tags, empty list)

## 7. Infrastructure Tests

- [ ] 7.1 Write unit tests for rate limiting middleware (within limit, exceeded, window reset)
- [ ] 7.2 Write unit tests for error response format (internal exception, validation error, HTTP exception)
- [ ] 7.3 Write unit tests for pagination defaults (default values, limit capping at 20)
- [ ] 7.4 Write unit tests for DI container resolution and session management (commit on success, rollback on exception)

## 8. E2E Integration Tests

- [ ] 8.1 Write E2E test for full user lifecycle (register -> login -> update -> get current user)
- [ ] 8.2 Write E2E test for article lifecycle (create -> read -> update -> delete)
- [ ] 8.3 Write E2E test for social features (follow -> feed -> comment -> favorite -> unfavorite -> unfollow)
