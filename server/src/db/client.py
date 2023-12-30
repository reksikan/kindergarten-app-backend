import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import _AsyncSessionContextManager, AsyncSession

logger = logging.Logger(__name__)


class DBClient:

    def __init__(self, async_engine: AsyncEngine):
        self._async_engine = async_engine
        self._async_session = async_sessionmaker(
            self._async_engine,
            expire_on_commit=False,
        )

    def session(self) -> _AsyncSessionContextManager[AsyncSession]:
        return self._async_session.begin()

    async def healthcheck(self) -> bool:
        try:
            async with self.session() as session:
                await session.execute(text('CREATE TEMPORARY TABLE test (testclmn TEXT) ON COMMIT DROP;'))
                return True
        except Exception:
            logger.exception('Database healthcheck failed')
            return False