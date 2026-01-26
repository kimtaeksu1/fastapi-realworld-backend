from sqlalchemy.ext.asyncio import AsyncSession

from conduit.dtos.domain.tag import TagDTO
from conduit.dtos.records.tag import TagRecordDTO
from conduit.interfaces.repositories.tag import ITagRepository
from conduit.interfaces.services.tag import ITagService


class TagService(ITagService):
    """Service to handle article tags logic."""

    def __init__(self, tag_repo: ITagRepository):
        self._tag_repo = tag_repo

    async def get_all_tags(self, session: AsyncSession) -> list[TagDTO]:
        tags = await self._tag_repo.list(session=session)
        return [self._to_tag_dto(tag) for tag in tags]

    @staticmethod
    def _to_tag_dto(record: TagRecordDTO) -> TagDTO:
        return TagDTO(id=record.id, tag=record.tag, created_at=record.created_at)
