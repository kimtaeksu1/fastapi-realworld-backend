"""
Unit tests for favorites (via article service).
Covers: OpenSpec specs/favorites/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.core.exceptions import (
    ArticleAlreadyFavoritedException,
    ArticleNotFavoritedException,
    ArticleNotFoundException,
)
from conduit.dtos.domain.article import ArticleDTO
from conduit.dtos.domain.user import UserDTO
from conduit.interfaces.services.article import IArticleService

# --- Requirement: Favorite article ---


@pytest.mark.anyio
async def test_favorite_article_success(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Successfully favorite an article"""
    article = await article_service.add_article_into_favorites(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert article.favorited is True
    assert article.favorites_count == 1


@pytest.mark.anyio
async def test_favorite_already_favorited(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Favorite already-favorited article"""
    await article_service.add_article_into_favorites(
        session=session, slug=test_article.slug, current_user=test_user
    )
    with pytest.raises(ArticleAlreadyFavoritedException):
        await article_service.add_article_into_favorites(
            session=session, slug=test_article.slug, current_user=test_user
        )


@pytest.mark.anyio
async def test_favorite_nonexistent_article(
    session: AsyncSession, article_service: IArticleService, test_user: UserDTO
) -> None:
    """Scenario: Favorite non-existent article"""
    with pytest.raises(ArticleNotFoundException):
        await article_service.add_article_into_favorites(
            session=session, slug="no-such-slug", current_user=test_user
        )


# --- Requirement: Unfavorite article ---


@pytest.mark.anyio
async def test_unfavorite_article_success(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Successfully unfavorite an article"""
    await article_service.add_article_into_favorites(
        session=session, slug=test_article.slug, current_user=test_user
    )
    article = await article_service.remove_article_from_favorites(
        session=session, slug=test_article.slug, current_user=test_user
    )
    assert article.favorited is False
    assert article.favorites_count == 0


@pytest.mark.anyio
async def test_unfavorite_not_favorited(
    session: AsyncSession,
    article_service: IArticleService,
    test_user: UserDTO,
    test_article: ArticleDTO,
) -> None:
    """Scenario: Unfavorite not-favorited article"""
    with pytest.raises(ArticleNotFavoritedException):
        await article_service.remove_article_from_favorites(
            session=session, slug=test_article.slug, current_user=test_user
        )


@pytest.mark.anyio
async def test_unfavorite_nonexistent_article(
    session: AsyncSession, article_service: IArticleService, test_user: UserDTO
) -> None:
    """Scenario: Unfavorite non-existent article"""
    with pytest.raises(ArticleNotFoundException):
        await article_service.remove_article_from_favorites(
            session=session, slug="no-such-slug", current_user=test_user
        )
