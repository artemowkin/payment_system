from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func

from ..project.db import BaseCommand

from ..users.models import User
from .models import Merchant
from .services.crypto import generate_tokens


class InitMerchantCommand(BaseCommand):
    depends_on = ('InitUserCommand', )

    async def run_command(self):
        async with self._session() as session:
            stmt = select(func.count('*')).select_from(Merchant)
            result = await session.execute(stmt)
            if result.scalar_one():
                return

            session: AsyncSession
            stmt = select(User)
            result = await session.execute(stmt)
            user = result.scalar_one()

            tokens = generate_tokens()
            stmt = insert(Merchant).values(
                slug='init_merchant',
                public_key=tokens.public_key,
                private_key=tokens.private_key,
                user_id=user.uuid,
            )
            await session.execute(stmt)
            await session.commit()
