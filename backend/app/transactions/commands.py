from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func

from ..project.db import BaseCommand
from ..project.utils import get_absolute_uri

from ..users.models import User
from ..merchants.models import Merchant
from .models import Transaction


class InitTransactionCommand(BaseCommand):
    depends_on = ('InitMerchantCommand', 'InitUserCommand')

    async def run_command(self):
        async with self._session() as session:
            stmt = select(func.count('*')).select_from(Transaction)
            result = await session.execute(stmt)
            if result.scalar_one():
                return

            stmt = select(Merchant)
            result = await session.execute(stmt)
            merchant = result.scalar_one()

            stmt = insert(Transaction).values(
                status='completed',
                type='deposit',
                merchant_id=merchant.uuid,
                amount=150,
                currency='RUB',
                redirect_url=get_absolute_uri('/example_integration'),
                card_info='5123'
            )
            await session.execute(stmt)

            await session.commit()
