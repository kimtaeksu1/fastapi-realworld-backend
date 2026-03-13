"""
Unit tests for authentication service.
Covers: OpenSpec specs/authentication/spec.md
"""

import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    EmailAlreadyTakenException,
    IncorrectJWTTokenException,
    IncorrectLoginInputException,
    UserNameAlreadyTakenException,
)
from conduit.dtos.domain.user import CreateUserDTO, UserDTO
from conduit.interfaces.services.auth import IUserAuthService
from conduit.interfaces.services.auth_token import IAuthTokenService
from conduit.interfaces.services.user import IUserService
from conduit.services.auth_token import AuthTokenService

# --- Requirement: User registration ---


@pytest.mark.anyio
async def test_sign_up_user_success(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Successful registration"""
    create_dto = CreateUserDTO(
        username="newuser", email="newuser@example.com", password="password123"
    )
    user, token = await user_auth_service.sign_up_user(
        session=session, user_to_create=create_dto
    )
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.anyio
async def test_sign_up_duplicate_email(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Duplicate email"""
    create_dto = CreateUserDTO(
        username="user1", email="dup@example.com", password="password123"
    )
    await user_auth_service.sign_up_user(session=session, user_to_create=create_dto)

    create_dto2 = CreateUserDTO(
        username="user2", email="dup@example.com", password="password123"
    )
    with pytest.raises(EmailAlreadyTakenException):
        await user_auth_service.sign_up_user(
            session=session, user_to_create=create_dto2
        )


@pytest.mark.anyio
async def test_sign_up_duplicate_username(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Duplicate username"""
    create_dto = CreateUserDTO(
        username="dupname", email="a@example.com", password="password123"
    )
    await user_auth_service.sign_up_user(session=session, user_to_create=create_dto)

    create_dto2 = CreateUserDTO(
        username="dupname", email="b@example.com", password="password123"
    )
    with pytest.raises(UserNameAlreadyTakenException):
        await user_auth_service.sign_up_user(
            session=session, user_to_create=create_dto2
        )


# --- Requirement: User login ---


@pytest.mark.anyio
async def test_sign_in_user_success(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Successful login"""
    create_dto = CreateUserDTO(
        username="loginuser", email="login@example.com", password="password123"
    )
    await user_auth_service.sign_up_user(session=session, user_to_create=create_dto)

    from conduit.dtos.domain.user import LoginUserDTO

    login_dto = LoginUserDTO(email="login@example.com", password="password123")
    user, token = await user_auth_service.sign_in_user(
        session=session, user_to_login=login_dto
    )
    assert user.email == "login@example.com"
    assert isinstance(token, str)


@pytest.mark.anyio
async def test_sign_in_nonexistent_email(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Non-existent email"""
    from conduit.dtos.domain.user import LoginUserDTO

    login_dto = LoginUserDTO(email="nobody@example.com", password="password123")
    with pytest.raises(IncorrectLoginInputException):
        await user_auth_service.sign_in_user(session=session, user_to_login=login_dto)


@pytest.mark.anyio
async def test_sign_in_wrong_password(
    session: AsyncSession, user_auth_service: IUserAuthService
) -> None:
    """Scenario: Incorrect password"""
    create_dto = CreateUserDTO(
        username="wrongpw", email="wrongpw@example.com", password="password123"
    )
    await user_auth_service.sign_up_user(session=session, user_to_create=create_dto)

    from conduit.dtos.domain.user import LoginUserDTO

    login_dto = LoginUserDTO(email="wrongpw@example.com", password="wrongpassword")
    with pytest.raises(IncorrectLoginInputException):
        await user_auth_service.sign_in_user(session=session, user_to_login=login_dto)


# --- Requirement: JWT token format ---


def test_jwt_generate_and_parse() -> None:
    """Scenario: Valid token accepted"""
    service = AuthTokenService(
        secret_key="testsecret", token_expiration_minutes=60, algorithm="HS256"
    )
    user = UserDTO(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hash",
        bio="",
        image="",
        created_at=datetime.datetime.now(),
    )
    token = service.generate_jwt_token(user=user)
    payload = service.parse_jwt_token(token=token)
    assert payload.user_id == 1
    assert payload.username == "testuser"


def test_jwt_invalid_token() -> None:
    """Scenario: Invalid token rejected"""
    service = AuthTokenService(
        secret_key="testsecret", token_expiration_minutes=60, algorithm="HS256"
    )
    with pytest.raises(IncorrectJWTTokenException):
        service.parse_jwt_token(token="invalid.token.here")


def test_jwt_expired_token() -> None:
    """Scenario: Expired token rejected"""
    service = AuthTokenService(
        secret_key="testsecret", token_expiration_minutes=-1, algorithm="HS256"
    )
    user = UserDTO(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hash",
        bio="",
        image="",
        created_at=datetime.datetime.now(),
    )
    token = service.generate_jwt_token(user=user)
    with pytest.raises(IncorrectJWTTokenException):
        service.parse_jwt_token(token=token)
