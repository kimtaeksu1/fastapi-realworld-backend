"""
Unit tests for user management service.
Covers: OpenSpec specs/user-management/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    EmailAlreadyTakenException,
    UserNameAlreadyTakenException,
    UserNotFoundException,
)
from conduit.dtos.domain.user import CreateUserDTO, UpdateUserDTO, UserDTO
from conduit.interfaces.services.user import IUserService

# --- Requirement: Get current user ---


@pytest.mark.anyio
async def test_get_user_by_id(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Authenticated user retrieves own profile"""
    user = await user_service.get_user_by_id(session=session, user_id=test_user.id)
    assert user.id == test_user.id
    assert user.username == test_user.username
    assert user.email == test_user.email


@pytest.mark.anyio
async def test_get_user_by_id_not_found(
    session: AsyncSession, user_service: IUserService
) -> None:
    """Scenario: User not found"""
    with pytest.raises(UserNotFoundException):
        await user_service.get_user_by_id(session=session, user_id=99999)


# --- Requirement: Update current user ---


@pytest.mark.anyio
async def test_update_username(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update username only"""
    update_dto = UpdateUserDTO(username="newname")
    updated = await user_service.update_user(
        session=session, current_user=test_user, user_to_update=update_dto
    )
    assert updated.username == "newname"
    assert updated.email == test_user.email


@pytest.mark.anyio
async def test_update_email(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update email only"""
    update_dto = UpdateUserDTO(email="newemail@example.com")
    updated = await user_service.update_user(
        session=session, current_user=test_user, user_to_update=update_dto
    )
    assert updated.email == "newemail@example.com"
    assert updated.username == test_user.username


@pytest.mark.anyio
async def test_update_bio_and_image(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update bio and image"""
    update_dto = UpdateUserDTO(bio="New bio", image="https://example.com/img.png")
    updated = await user_service.update_user(
        session=session, current_user=test_user, user_to_update=update_dto
    )
    assert updated.bio == "New bio"
    assert updated.image == "https://example.com/img.png"


@pytest.mark.anyio
async def test_update_duplicate_email(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update with duplicate email"""
    other_dto = CreateUserDTO(
        username="other", email="taken@example.com", password="password123"
    )
    await user_service.create_user(session=session, user_to_create=other_dto)

    update_dto = UpdateUserDTO(email="taken@example.com")
    with pytest.raises(EmailAlreadyTakenException):
        await user_service.update_user(
            session=session, current_user=test_user, user_to_update=update_dto
        )


@pytest.mark.anyio
async def test_update_duplicate_username(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update with duplicate username"""
    other_dto = CreateUserDTO(
        username="taken", email="other@example.com", password="password123"
    )
    await user_service.create_user(session=session, user_to_create=other_dto)

    update_dto = UpdateUserDTO(username="taken")
    with pytest.raises(UserNameAlreadyTakenException):
        await user_service.update_user(
            session=session, current_user=test_user, user_to_update=update_dto
        )


@pytest.mark.anyio
async def test_update_same_email_no_error(
    session: AsyncSession, user_service: IUserService, test_user: UserDTO
) -> None:
    """Scenario: Update with same email (no change)"""
    update_dto = UpdateUserDTO(email=test_user.email)
    updated = await user_service.update_user(
        session=session, current_user=test_user, user_to_update=update_dto
    )
    assert updated.email == test_user.email
