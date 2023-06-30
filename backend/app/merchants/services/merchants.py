from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .crypto import generate_tokens
from ..schemas import DbMerchant, MerchantIn
from ...users.schemas import DbUser
from ..models import Merchant


def _handle_unique_violation(func):

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant with this slug already exists")

    return wrapper


class MerchantsSet:

    def __init__(self, session: AsyncSession, user: DbUser):
        self._session = session
        self._user = user

    @_handle_unique_violation
    async def create(self, merchant_data: MerchantIn) -> DbMerchant:
        tokens = generate_tokens()
        stmt = insert(Merchant).returning(Merchant).values(**merchant_data.dict(), **tokens.dict(), user_id=self._user.uuid)
        result = await self._session.execute(stmt)
        return DbMerchant.from_orm(result.scalar_one())

    async def all(self) -> list[DbMerchant]:
        stmt = select(Merchant).where(Merchant.user_id == self._user.uuid, Merchant.blocked == False)
        result = await self._session.execute(stmt)
        return [DbMerchant.from_orm(m) for m in result.scalars()]

    async def get_concrete(self, uuid: UUID) -> DbMerchant:
        stmt = select(Merchant).where(Merchant.user_id == self._user.uuid, Merchant.uuid == str(uuid), Merchant.blocked == False)
        result = await self._session.execute(stmt)
        result_scalar = result.scalar_one_or_none()
        if not result_scalar:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no merchant with uuid `{uuid}`")

        return DbMerchant.from_orm(result_scalar)

    @classmethod
    async def get_concrete_anonymous(cls, session: AsyncSession, uuid: UUID) -> DbMerchant:
        stmt = select(Merchant).where(Merchant.uuid == str(uuid), Merchant.blocked == False)
        result = await session.execute(stmt)
        result_scalar = result.scalar_one_or_none()
        if not result_scalar:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no merchant with uuid `{uuid}`")

        return DbMerchant.from_orm(result_scalar)

    async def regenerate_tokens(self, merchant: DbMerchant) -> DbMerchant:
        new_tokens = generate_tokens()
        stmt = update(Merchant).returning(Merchant).values(**new_tokens.dict()).where(Merchant.uuid == merchant.uuid)
        result = await self._session.execute(stmt)
        return DbMerchant.from_orm(result.scalar_one())

    async def block(self, merchant: DbMerchant) -> None:
        stmt = update(Merchant).values(blocked=True).where(Merchant.uuid == merchant.uuid)
        await self._session.execute(stmt)
