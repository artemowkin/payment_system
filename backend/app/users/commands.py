from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func

from ..project.db import BaseCommand

from .models import User
from .services import pwd_context


class InitUserCommand(BaseCommand):

    async def run_command(self):
        async with self._session() as session:
            stmt = select(func.count('*')).select_from(User)
            result = await session.execute(stmt)
            if result.scalar_one():
                return

            stmt = insert(User).values(
                email='admin@gmail.com',
                first_name='Ivan',
                last_name='Ivanov',
                middle_name='Ivanovich',
                password=pwd_context.hash('Qwerty123')
            )
            await session.execute(stmt)
            await session.commit()
