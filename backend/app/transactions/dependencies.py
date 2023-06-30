from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..merchants.dependencies import use_merchants_set
from ..merchants.services.merchants import MerchantsSet
from ..users.dependencies import auth_required
from ..users.schemas import DbUser
from ..project.dependencies import use_session
from .services.transactions import TransactionsSet


def use_transactions_set(user: DbUser = Depends(auth_required),
                         merchants_set: MerchantsSet = Depends(use_merchants_set),
                         session: AsyncSession = Depends(use_session)):
    return TransactionsSet(session=session, user=user, merchants_set=merchants_set)
