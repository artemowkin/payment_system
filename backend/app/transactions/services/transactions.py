from typing import Literal
from uuid import UUID
import secrets
from datetime import timedelta

from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text

from ...users.schemas import DbUser
from ...merchants.services.merchants import MerchantsSet
from ...merchants.schemas import DbMerchant
from ...merchants.models import Merchant
from ...project.redis import redis_db
from ..schemas import TransactionIn, DbTransaction, TransactionStatuses, CardInfo
from ..models import Transaction
from .signatures import validate_signature


async def generate_transaction_key(transaction: DbTransaction) -> str:
    key = secrets.token_hex(30)
    await redis_db.set(f'transaction:{key}', str(transaction.uuid), ex=timedelta(hours=12))
    return key


async def get_transaction_id_by_key(transaction_key: str) -> str:
    transaction_id = await redis_db.get(f"transaction:{transaction_key}")
    if not transaction_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction has expired or doesn't exist")

    return transaction_id.decode()


async def delete_transaction_key(transaction_key: str):
    await redis_db.delete(f'transaction:{transaction_key}')


class TransactionsSet:

    def __init__(self, session: AsyncSession, user: DbUser, merchants_set: MerchantsSet):
        self._session = session
        self._user = user
        self._merchants_set = merchants_set

    @classmethod
    async def create(cls, session: AsyncSession, transaction_data: TransactionIn) -> DbTransaction:
        merchant = await MerchantsSet.get_concrete_anonymous(session, transaction_data.merchant_id)
        if transaction_data.public_key != merchant.public_key:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Incorrect public key")

        if not validate_signature(transaction_data, merchant):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Incorrect signature")

        stmt = insert(Transaction).returning(Transaction).options(
            selectinload(Transaction.merchant)
        ).values(**transaction_data.dict(exclude={'signature', 'public_key'}), status=TransactionStatuses.created)
        result = await session.execute(stmt)
        return DbTransaction.from_orm(result.scalar_one())

    async def get_all(self, merchant: DbMerchant | None,
                      ord_by: str = 'datetime', ord: Literal['ASC', 'DESC'] = 'DESC') -> list[DbTransaction]:
        stmt = select(Transaction).options(
            selectinload(Transaction.merchant)
        ).join(Merchant).where(Merchant.user_id == self._user.uuid).order_by(text(f"{ord_by} {ord}"))
        if merchant:
            stmt = stmt.where(Transaction.merchant_id == merchant.uuid)

        result = await self._session.execute(stmt)
        return [DbTransaction.from_orm(transaction) for transaction in result.scalars()]

    @classmethod
    async def get_anonymous(cls, session: AsyncSession, transaction_key: str) -> DbTransaction:
        transaction_id = await get_transaction_id_by_key(transaction_key)
        stmt = select(Transaction).options(
            selectinload(Transaction.merchant)
        ).where(Transaction.uuid == transaction_id)
        result = await session.execute(stmt)
        scalar = result.scalar()
        if not scalar:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect transaction key")

        return DbTransaction.from_orm(scalar)

    async def get_concrete(self, transaction_uuid: UUID) -> DbTransaction:
        stmt = select(Transaction).options(
            selectinload(Transaction.merchant)
        ).where(Transaction.uuid == transaction_uuid)
        result = await self._session.execute(stmt)
        scalar = result.scalar_one_or_none()
        if not scalar:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction with this uuid doesn't exist")

        return DbTransaction.from_orm(scalar)

    @classmethod
    async def apply_transaction(cls, session: AsyncSession, transaction: DbTransaction, card_info: CardInfo) -> str:
        if transaction.status != TransactionStatuses.created:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction already completed")

        stmt = update(Transaction).returning(Transaction).values(
            card_info=card_info.card_code[-4:], status=TransactionStatuses.completed
        ).where(Transaction.uuid == transaction.uuid)
        result = await session.execute(stmt)
        return result.scalar_one().redirect_url
