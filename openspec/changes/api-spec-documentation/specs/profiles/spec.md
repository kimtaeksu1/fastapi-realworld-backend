## ADDED Requirements

### Requirement: Get user profile
The system SHALL return a user's public profile via `GET /api/profiles/:username`. If the requester is authenticated, the response SHALL include whether the requester follows the target user.

**Response 200**: `{"profile": {"username": str, "bio": str|null, "image": str|null, "following": bool}}`

#### Scenario: Authenticated user views profile
- **WHEN** an authenticated user requests a profile of an existing user
- **THEN** the system returns 200 with profile data and `following` reflecting the actual follow status

#### Scenario: Unauthenticated user views profile
- **WHEN** an unauthenticated user requests a profile of an existing user
- **THEN** the system returns 200 with profile data and `following: false`

#### Scenario: Profile not found
- **WHEN** a user requests a profile with a non-existent username
- **THEN** the system returns 404 with `ProfileNotFoundException`

### Requirement: Follow user
The system SHALL allow authenticated users to follow another user via `POST /api/profiles/:username/follow`. Users SHALL NOT be able to follow themselves or follow a user they already follow.

**Response 200**: `{"profile": {"username": str, "bio": str|null, "image": str|null, "following": true}}`

#### Scenario: Successfully follow a user
- **WHEN** an authenticated user follows a user they are not yet following
- **THEN** the system creates the follow relationship and returns 200 with `following: true`

#### Scenario: Follow self
- **WHEN** an authenticated user tries to follow their own profile
- **THEN** the system returns 403 with `OwnProfileFollowingException`

#### Scenario: Follow already-followed user
- **WHEN** an authenticated user tries to follow a user they already follow
- **THEN** the system returns 400 with `ProfileAlreadyFollowedException`

#### Scenario: Follow non-existent user
- **WHEN** an authenticated user tries to follow a non-existent username
- **THEN** the system returns 404 with `UserNotFoundException`

### Requirement: Unfollow user
The system SHALL allow authenticated users to unfollow a user via `DELETE /api/profiles/:username/follow`. Users SHALL NOT be able to unfollow themselves or unfollow a user they do not follow.

**Response 200**: `{"profile": {"username": str, "bio": str|null, "image": str|null, "following": false}}`

#### Scenario: Successfully unfollow a user
- **WHEN** an authenticated user unfollows a user they currently follow
- **THEN** the system removes the follow relationship and returns 200 with `following: false`

#### Scenario: Unfollow self
- **WHEN** an authenticated user tries to unfollow their own profile
- **THEN** the system returns 403 with `OwnProfileFollowingException`

#### Scenario: Unfollow not-followed user
- **WHEN** an authenticated user tries to unfollow a user they do not follow
- **THEN** the system returns 400 with `ProfileNotFollowedFollowedException`
