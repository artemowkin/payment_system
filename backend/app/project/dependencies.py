from sqlalchemy.ext.asyncio import AsyncSession

from .db import async_session


async def use_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()