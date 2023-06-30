from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.dependencies import auth_required
from ..users.schemas import DbUser
from ..project.dependencies import use_session
from .services.merchants import MerchantsSet


def use_merchants_set(user: DbUser = Depends(auth_required), session: AsyncSession = Depends(use_session)) -> MerchantsSet:
    return MerchantsSet(session, user)
