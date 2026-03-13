## ADDED Requirements

### Requirement: Get current user
The system SHALL return the currently authenticated user's data via `GET /api/user`. This endpoint requires a valid JWT token.

**Response 200**: `{"user": {"id": int, "email": str, "username": str, "bio": str, "image": str, "token": str}}`

#### Scenario: Authenticated user retrieves own profile
- **WHEN** an authenticated user sends `GET /api/user`
- **THEN** the system returns 200 with the user's data including the current JWT token

#### Scenario: Unauthenticated request
- **WHEN** an unauthenticated user sends `GET /api/user`
- **THEN** the system returns 403 error

### Requirement: Update current user
The system SHALL allow authenticated users to update their profile via `PUT /api/user`. All fields are optional. The system SHALL validate uniqueness of email and username if changed. Empty strings are treated as None.

**Request**: `{"user": {"email?": EmailStr, "password?": str (min 8), "username?": str (min 3), "bio?": str, "image?": str}}`
**Response 200**: `{"user": {"id": int, "email": str, "username": str, "bio": str, "image": str, "token": str}}`

#### Scenario: Update username only
- **WHEN** an authenticated user sends a valid update with only username changed
- **THEN** the system returns 200 with updated user data, other fields unchanged

#### Scenario: Update email only
- **WHEN** an authenticated user sends a valid update with only email changed
- **THEN** the system returns 200 with updated user data

#### Scenario: Update password
- **WHEN** an authenticated user sends a valid update with a new password
- **THEN** the system hashes the new password and stores it, returning 200

#### Scenario: Update with duplicate email
- **WHEN** an authenticated user tries to change email to one already taken by another user
- **THEN** the system returns 400 with `EmailAlreadyTakenException`

#### Scenario: Update with duplicate username
- **WHEN** an authenticated user tries to change username to one already taken by another user
- **THEN** the system returns 400 with `UserNameAlreadyTakenException`

#### Scenario: Update with same email (no change)
- **WHEN** an authenticated user submits their current email in the update
- **THEN** the system does NOT raise a duplicate error and returns 200

#### Scenario: Empty string treated as None
- **WHEN** an authenticated user sends an empty string for a field
- **THEN** the field is treated as None (no update for that field)
