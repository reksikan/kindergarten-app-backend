from sqlalchemy import select

from src.db.repository.base import BaseRepository

from src.db.models.child import Child


class ChildrenRepository(BaseRepository):
    async def get_by_id(self, id_: int) -> Child | None:
        async with self._client.session() as session:
            return (
                await session.scalars(
                    select(Child)
                    .where(
                        Child.id == id_
                    )
                )
            ).one_or_none()