"""
Unit tests for comment service.
Covers: OpenSpec specs/comments/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    ArticleNotFoundException,
    CommentNotFoundException,
    CommentPermissionException,
)
from conduit.dtos.domain.article import ArticleDTO, CreateArticleDTO
from conduit.dtos.domain.comment import CreateCommentDTO
from conduit.dtos.domain.user import CreateUserDTO, UserDTO
from conduit.interfaces.services.article import IArticleService
from conduit.interfaces.services.comment import ICommentService
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


# --- Requirement: List article comments ---


@pytest.mark.anyio
async def test_get_comments_empty(
    session: AsyncSession, comment_service: ICommentService, test_article: ArticleDTO
) -> None:
    """Scenario: Get comments for article with no comments"""
    result = await comment_service.get_article_comments(
        session=session, slug=test_article.slug, current_user=None
    )
    assert result.comments == []
    assert result.comments_count == 0


@pytest.mark.anyio
async def test_get_comments_for_nonexistent_article(
    session: AsyncSession, comment_service: ICommentService
) -> None:
    """Scenario: Get comments for non-existent article"""
    with pytest.raises(ArticleNotFoundException):
        await comment_service.get_article_comments(
            session=session, slug="no-such-article", current_user=None
        )


# --- Requirement: Create comment ---


@pytest.mark.anyio
async def test_create_comment_success(
    session: AsyncSession,
    comment_service: ICommentService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Successfully create comment"""
    comment_dto = CreateCommentDTO(body="Great article!")
    comment = await comment_service.create_article_comment(
        session=session,
        slug=test_article.slug,
        comment_to_create=comment_dto,
        current_user=test_user,
    )
    assert comment.body == "Great article!"
    assert comment.author.username == test_user.username


@pytest.mark.anyio
async def test_create_comment_on_nonexistent_article(
    session: AsyncSession, comment_service: ICommentService, test_user: UserDTO
) -> None:
    """Scenario: Create comment on non-existent article"""
    comment_dto = CreateCommentDTO(body="Orphan comment")
    with pytest.raises(ArticleNotFoundException):
        await comment_service.create_article_comment(
            session=session,
            slug="nonexistent-slug",
            comment_to_create=comment_dto,
            current_user=test_user,
        )


@pytest.mark.anyio
async def test_list_comments_after_creation(
    session: AsyncSession,
    comment_service: ICommentService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Get comments (authenticated) after creating"""
    comment_dto = CreateCommentDTO(body="Hello from test")
    await comment_service.create_article_comment(
        session=session,
        slug=test_article.slug,
        comment_to_create=comment_dto,
        current_user=test_user,
    )
    result = await comment_service.get_article_comments(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert result.comments_count == 1
    assert result.comments[0].body == "Hello from test"


# --- Requirement: Delete comment ---


@pytest.mark.anyio
async def test_delete_comment_by_author(
    session: AsyncSession,
    comment_service: ICommentService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Author deletes own comment"""
    comment_dto = CreateCommentDTO(body="To be deleted")
    comment = await comment_service.create_article_comment(
        session=session,
        slug=test_article.slug,
        comment_to_create=comment_dto,
        current_user=test_user,
    )
    await comment_service.delete_article_comment(
        session=session,
        slug=test_article.slug,
        comment_id=comment.id,
        current_user=test_user,
    )
    result = await comment_service.get_article_comments(
        session=session, slug=test_article.slug, current_user=None
    )
    assert all(c.id != comment.id for c in result.comments)


@pytest.mark.anyio
async def test_delete_comment_non_author(
    session: AsyncSession,
    comment_service: ICommentService,
    user_service: IUserService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Non-author tries to delete comment"""
    comment_dto = CreateCommentDTO(body="Protected comment")
    comment = await comment_service.create_article_comment(
        session=session,
        slug=test_article.slug,
        comment_to_create=comment_dto,
        current_user=test_user,
    )
    other_user = await _create_user(
        session, user_service, "commentother", "co@example.com"
    )
    with pytest.raises(CommentPermissionException):
        await comment_service.delete_article_comment(
            session=session,
            slug=test_article.slug,
            comment_id=comment.id,
            current_user=other_user,
        )


@pytest.mark.anyio
async def test_delete_nonexistent_comment(
    session: AsyncSession,
    comment_service: ICommentService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Delete non-existent comment"""
    with pytest.raises(CommentNotFoundException):
        await comment_service.delete_article_comment(
            session=session,
            slug=test_article.slug,
            comment_id=99999,
            current_user=test_user,
        )
