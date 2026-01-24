from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.dtos.article import ArticleRecordDTO, CreateArticleDTO
from conduit.domain.dtos.user import CreateUserDTO, UserDTO
from conduit.domain.services.user import IUserService
from conduit.infrastructure.repositories.article import ArticleRepository


async def create_another_test_user(
    session: AsyncSession, user_service: IUserService
) -> UserDTO:
    create_user_dto = CreateUserDTO(
        username="temp-user", email="temp-user@gmail.com", password="password"
    )
    return await user_service.create_user(
        session=session, user_to_create=create_user_dto
    )


async def create_another_test_article(
    session: AsyncSession, article_repository: ArticleRepository, author_id: int
) -> ArticleRecordDTO:
    create_article_dto = CreateArticleDTO(
        title="One More Test Article",
        description="Test Description",
        body="Test Body Content",
        tags=["tag1", "tag2", "tag3"],
    )
    return await article_repository.add(
        session=session, author_id=author_id, create_item=create_article_dto
    )
