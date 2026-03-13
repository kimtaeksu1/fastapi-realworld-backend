"""
Unit tests for tag service.
Covers: OpenSpec specs/tags/spec.md
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.dtos.domain.article import ArticleDTO, CreateArticleDTO
from conduit.dtos.domain.user import UserDTO
from conduit.interfaces.services.article import IArticleService
from conduit.interfaces.services.tag import ITagService

# --- Requirement: List all tags ---


@pytest.mark.anyio
async def test_get_tags_empty(session: AsyncSession, tag_service: ITagService) -> None:
    """Scenario: Get tags when no tags exist"""
    tags = await tag_service.get_all_tags(session=session)
    assert tags == []


@pytest.mark.anyio
async def test_get_tags_with_articles(
    session: AsyncSession, tag_service: ITagService, test_article: ArticleDTO
) -> None:
    """Scenario: Get tags when tags exist"""
    tags = await tag_service.get_all_tags(session=session)
    tag_names = [t.tag for t in tags]
    assert len(tag_names) >= 1
    # test_article has tags ["tag1", "tag2"] from the fixture
    assert "tag1" in tag_names
    assert "tag2" in tag_names
