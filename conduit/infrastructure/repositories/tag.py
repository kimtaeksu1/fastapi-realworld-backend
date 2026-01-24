from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.dtos.tag import TagRecordDTO
from conduit.domain.repositories.tag import ITagRepository
from conduit.infrastructure.models import Tag


class TagRepository(ITagRepository):
    """Repository for Tag model."""

    @staticmethod
    def _to_tag_record_dto(model: Tag) -> TagRecordDTO:
        return TagRecordDTO(id=model.id, tag=model.tag, created_at=model.created_at)

    async def list(self, session: AsyncSession) -> list[TagRecordDTO]:
        query = select(Tag)
        tags = await session.scalars(query)
        return [self._to_tag_record_dto(tag) for tag in tags]
