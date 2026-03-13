"""
Unit tests for profile service.
Covers: OpenSpec specs/profiles/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    OwnProfileFollowingException,
    ProfileAlreadyFollowedException,
    ProfileNotFollowedFollowedException,
    ProfileNotFoundException,
)
from conduit.dtos.domain.user import CreateUserDTO, UserDTO
from conduit.interfaces.services.profile import IProfileService
from conduit.interfaces.services.user import IUserService


async def _create_user(
    session: AsyncSession, user_service: IUserService, username: str, email: str
) -> UserDTO:
    return await user_service.create_user(
        session=session,
        user_to_create=CreateUserDTO(
            username=username, email=email, password="password123"
        ),
    )


# --- Requirement: Get user profile ---


@pytest.mark.anyio
async def test_get_profile_authenticated(
    session: AsyncSession,
    profile_service: IProfileService,
    user_service: IUserService,
    test_user: UserDTO,
) -> None:
    """Scenario: Authenticated user views profile"""
    target = await _create_user(session, user_service, "target", "target@example.com")
    profile = await profile_service.get_profile_by_username(
        session=session, username=target.username, current_user=test_user
    )
    assert profile.username == "target"
    assert profile.following is False


@pytest.mark.anyio
async def test_get_profile_unauthenticated(
    session: AsyncSession, profile_service: IProfileService, test_user: UserDTO
) -> None:
    """Scenario: Unauthenticated user views profile"""
    profile = await profile_service.get_profile_by_username(
        session=session, username=test_user.username, current_user=None
    )
    assert profile.username == test_user.username
    assert profile.following is False


@pytest.mark.anyio
async def test_get_profile_not_found(
    session: AsyncSession, profile_service: IProfileService
) -> None:
    """Scenario: Profile not found"""
    with pytest.raises(ProfileNotFoundException):
        await profile_service.get_profile_by_username(
            session=session, username="nonexistent", current_user=None
        )


# --- Requirement: Follow user ---


@pytest.mark.anyio
async def test_follow_user_success(
    session: AsyncSession,
    profile_service: IProfileService,
    user_service: IUserService,
    test_user: UserDTO,
) -> None:
    """Scenario: Successfully follow a user"""
    target = await _create_user(session, user_service, "followtarget", "ft@example.com")
    await profile_service.follow_user(
        session=session, username=target.username, current_user=test_user
    )
    profile = await profile_service.get_profile_by_username(
        session=session, username=target.username, current_user=test_user
    )
    assert profile.following is True


@pytest.mark.anyio
async def test_follow_self(
    session: AsyncSession, profile_service: IProfileService, test_user: UserDTO
) -> None:
    """Scenario: Follow self"""
    with pytest.raises(OwnProfileFollowingException):
        await profile_service.follow_user(
            session=session, username=test_user.username, current_user=test_user
        )


@pytest.mark.anyio
async def test_follow_already_followed(
    session: AsyncSession,
    profile_service: IProfileService,
    user_service: IUserService,
    test_user: UserDTO,
) -> None:
    """Scenario: Follow already-followed user"""
    target = await _create_user(session, user_service, "alreadyf", "af@example.com")
    await profile_service.follow_user(
        session=session, username=target.username, current_user=test_user
    )
    with pytest.raises(ProfileAlreadyFollowedException):
        await profile_service.follow_user(
            session=session, username=target.username, current_user=test_user
        )


# --- Requirement: Unfollow user ---


@pytest.mark.anyio
async def test_unfollow_user_success(
    session: AsyncSession,
    profile_service: IProfileService,
    user_service: IUserService,
    test_user: UserDTO,
) -> None:
    """Scenario: Successfully unfollow a user"""
    target = await _create_user(session, user_service, "unftarget", "unf@example.com")
    await profile_service.follow_user(
        session=session, username=target.username, current_user=test_user
    )
    await profile_service.unfollow_user(
        session=session, username=target.username, current_user=test_user
    )
    profile = await profile_service.get_profile_by_username(
        session=session, username=target.username, current_user=test_user
    )
    assert profile.following is False


@pytest.mark.anyio
async def test_unfollow_self(
    session: AsyncSession, profile_service: IProfileService, test_user: UserDTO
) -> None:
    """Scenario: Unfollow self"""
    with pytest.raises(OwnProfileFollowingException):
        await profile_service.unfollow_user(
            session=session, username=test_user.username, current_user=test_user
        )


@pytest.mark.anyio
async def test_unfollow_not_followed(
    session: AsyncSession,
    profile_service: IProfileService,
    user_service: IUserService,
    test_user: UserDTO,
) -> None:
    """Scenario: Unfollow not-followed user"""
    target = await _create_user(session, user_service, "notfollowed", "nf@example.com")
    with pytest.raises(ProfileNotFollowedFollowedException):
        await profile_service.unfollow_user(
            session=session, username=target.username, current_user=test_user
        )
