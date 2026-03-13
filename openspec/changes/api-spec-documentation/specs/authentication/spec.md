## ADDED Requirements

### Requirement: User registration
The system SHALL allow new users to register by providing username, email, and password via `POST /api/users`. The system SHALL hash the password before storage, validate uniqueness of email and username, and return a JWT token upon successful registration.

**Request**: `{"user": {"username": str (min 3), "email": EmailStr, "password": str (min 8)}}`
**Response 200**: `{"user": {"id": int, "email": str, "username": str, "bio": str, "image": str, "token": str}}`

#### Scenario: Successful registration
- **WHEN** a valid registration request is submitted with unique email and username
- **THEN** the system creates the user, returns 200 with user data and JWT token

#### Scenario: Duplicate email
- **WHEN** a registration request is submitted with an email that already exists
- **THEN** the system returns 400 with `EmailAlreadyTakenException` and error `{"email": ["user with this email already exists."]}`

#### Scenario: Duplicate username
- **WHEN** a registration request is submitted with a username that already exists
- **THEN** the system returns 400 with `UserNameAlreadyTakenException` and error `{"username": ["user with this username already exists."]}`

#### Scenario: Invalid email format
- **WHEN** a registration request is submitted with an invalid email
- **THEN** the system returns 422 with `RequestValidationError`

#### Scenario: Password too short
- **WHEN** a registration request is submitted with a password shorter than 8 characters
- **THEN** the system returns 422 with `RequestValidationError`

#### Scenario: Username too short
- **WHEN** a registration request is submitted with a username shorter than 3 characters
- **THEN** the system returns 422 with `RequestValidationError`

### Requirement: User login
The system SHALL authenticate users via `POST /api/users/login` by verifying email and password. On success, the system SHALL return user data with a JWT token. On failure, the system SHALL return a generic error without revealing whether the email or password was incorrect.

**Request**: `{"user": {"email": EmailStr, "password": str (min 8)}}`
**Response 200**: `{"user": {"email": str, "username": str, "bio": str, "image": str, "token": str}}`

#### Scenario: Successful login
- **WHEN** a valid email and correct password are provided
- **THEN** the system returns 200 with user data and JWT token

#### Scenario: Non-existent email
- **WHEN** a login request is submitted with an email not in the database
- **THEN** the system returns 400 with `IncorrectLoginInputException` and errors on both email and password fields

#### Scenario: Incorrect password
- **WHEN** a login request is submitted with a valid email but wrong password
- **THEN** the system returns 400 with `IncorrectLoginInputException` and errors on both email and password fields

### Requirement: JWT token format
The system SHALL use `Authorization: Token {jwt}` header format (not Bearer). Tokens are issued with configurable expiration (`jwt_token_expiration_minutes`) and signed with `jwt_secret_key` using the configured `jwt_algorithm`.

#### Scenario: Valid token accepted
- **WHEN** a request includes a valid, non-expired JWT in `Authorization: Token xxx.yyy.zzz` format
- **THEN** the system authenticates the user and proceeds with the request

#### Scenario: Invalid token rejected
- **WHEN** a request includes an invalid or expired JWT token
- **THEN** the system returns 403 with `IncorrectJWTTokenException`

#### Scenario: Missing token on protected endpoint
- **WHEN** a request to a protected endpoint has no Authorization header
- **THEN** the system returns 403 error
