"""
Unit tests for article service.
Covers: OpenSpec specs/articles/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import ArticleNotFoundException, ArticlePermissionException
from conduit.dtos.domain.article import ArticleDTO, CreateArticleDTO, UpdateArticleDTO
from conduit.dtos.domain.user import CreateUserDTO, UserDTO
from conduit.interfaces.services.article import IArticleService
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


# --- Requirement: Create article ---


@pytest.mark.anyio
async def test_create_article_with_tags(
    session: AsyncSession, article_service: IArticleService, test_user: UserDTO
) -> None:
    """Scenario: Create article with tags"""
    create_dto = CreateArticleDTO(
        title="Test Article Title",
        description="Test description content",
        body="Test body content here",
        tags=["python", "fastapi"],
    )
    article = await article_service.create_new_article(
        session=session, author_id=test_user.id, article_to_create=create_dto
    )
    assert article.title == "Test Article Title"
    assert article.favorited is False
    assert article.favorites_count == 0
    assert article.author.username == test_user.username
    assert set(article.tags) == {"python", "fastapi"}


@pytest.mark.anyio
async def test_create_article_without_tags(
    session: AsyncSession, article_service: IArticleService, test_user: UserDTO
) -> None:
    """Scenario: Create article without tags"""
    create_dto = CreateArticleDTO(
        title="No Tags Article",
        description="Test description content",
        body="Test body content here",
        tags=[],
    )
    article = await article_service.create_new_article(
        session=session, author_id=test_user.id, article_to_create=create_dto
    )
    assert article.tags == []


# --- Requirement: Get article by slug ---


@pytest.mark.anyio
async def test_get_article_by_slug_authenticated(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Get existing article (authenticated)"""
    article = await article_service.get_article_by_slug(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert article.slug == test_article.slug
    assert article.title == test_article.title


@pytest.mark.anyio
async def test_get_article_by_slug_unauthenticated(
    session: AsyncSession, article_service: IArticleService, test_article: ArticleDTO
) -> None:
    """Scenario: Get existing article (unauthenticated)"""
    article = await article_service.get_article_by_slug(
        session=session, slug=test_article.slug, current_user=None
    )
    assert article.favorited is False
    assert article.author.following is False


@pytest.mark.anyio
async def test_get_article_not_found(
    session: AsyncSession, article_service: IArticleService
) -> None:
    """Scenario: Article not found"""
    with pytest.raises(ArticleNotFoundException):
        await article_service.get_article_by_slug(
            session=session, slug="nonexistent-slug", current_user=None
        )


# --- Requirement: Update article ---


@pytest.mark.anyio
async def test_update_article_by_author(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Author updates own article"""
    update_dto = UpdateArticleDTO(title="Updated Title", description=None, body=None)
    updated = await article_service.update_article_by_slug(
        session=session,
        slug=test_article.slug,
        article_to_update=update_dto,
        current_user=test_user,
    )
    assert updated.title == "Updated Title"


@pytest.mark.anyio
async def test_update_article_non_author(
    session: AsyncSession,
    article_service: IArticleService,
    user_service: IUserService,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Non-author tries to update"""
    other_user = await _create_user(session, user_service, "other", "other@example.com")
    update_dto = UpdateArticleDTO(title="Hacked Title", description=None, body=None)
    with pytest.raises(ArticlePermissionException):
        await article_service.update_article_by_slug(
            session=session,
            slug=test_article.slug,
            article_to_update=update_dto,
            current_user=other_user,
        )


# --- Requirement: Delete article ---


@pytest.mark.anyio
async def test_delete_article_by_author(
    session: AsyncSession, article_service: IArticleService, test_user: UserDTO
) -> None:
    """Scenario: Author deletes own article"""
    create_dto = CreateArticleDTO(
        title="To Be Deleted",
        description="Delete description",
        body="Delete body content",
        tags=[],
    )
    article = await article_service.create_new_article(
        session=session, author_id=test_user.id, article_to_create=create_dto
    )
    await article_service.delete_article_by_slug(
        session=session, slug=article.slug, current_user=test_user
    )
    with pytest.raises(ArticleNotFoundException):
        await article_service.get_article_by_slug(
            session=session, slug=article.slug, current_user=None
        )


@pytest.mark.anyio
async def test_delete_article_non_author(
    session: AsyncSession,
    article_service: IArticleService,
    user_service: IUserService,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Non-author tries to delete"""
    other_user = await _create_user(
        session, user_service, "delother", "delother@example.com"
    )
    with pytest.raises(ArticlePermissionException):
        await article_service.delete_article_by_slug(
            session=session, slug=test_article.slug, current_user=other_user
        )


# --- Requirement: Global article feed ---


@pytest.mark.anyio
async def test_global_feed_unfiltered(
    session: AsyncSession, article_service: IArticleService, test_article: ArticleDTO
) -> None:
    """Scenario: Unfiltered global feed"""
    feed = await article_service.get_articles_by_filters(
        session=session, current_user=None, limit=20, offset=0
    )
    assert feed.articles_count >= 1
    assert len(feed.articles) >= 1


@pytest.mark.anyio
async def test_global_feed_filter_by_tag(
    session: AsyncSession, article_service: IArticleService, test_article: ArticleDTO
) -> None:
    """Scenario: Filter by tag"""
    feed = await article_service.get_articles_by_filters(
        session=session, current_user=None, limit=20, offset=0, tag="tag1"
    )
    for article in feed.articles:
        assert "tag1" in article.tags


@pytest.mark.anyio
async def test_global_feed_filter_by_author(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Filter by author"""
    feed = await article_service.get_articles_by_filters(
        session=session,
        current_user=None,
        limit=20,
        offset=0,
        author=test_user.username,
    )
    assert feed.articles_count >= 1
    for article in feed.articles:
        assert article.author.username == test_user.username


# --- Requirement: Personal article feed ---


@pytest.mark.anyio
async def test_personal_feed_with_followings(
    session: AsyncSession,
    article_service: IArticleService,
    user_service: IUserService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Authenticated user gets feed (initially empty if not following anyone)"""
    feed = await article_service.get_articles_feed(
        session=session, current_user=test_user, limit=20, offset=0
    )
    # test_user doesn't follow anyone, so feed should be empty
    assert feed.articles_count == 0
    assert len(feed.articles) == 0
