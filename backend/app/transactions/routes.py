from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    TransactionOut, TransactionIn, RedirectResponse, CardInfo, TransactionCreateResponse,
    TransactionOutAnonymous
)
from .services.transactions import TransactionsSet, generate_transaction_key, delete_transaction_key
from .dependencies import use_transactions_set
from ..merchants.services.merchants import MerchantsSet
from ..merchants.dependencies import use_merchants_set
from ..project.utils import get_absolute_uri
from ..project.dependencies import use_session


router = APIRouter()


@router.post('/', response_model=TransactionCreateResponse)
async def create_transaction(transaction_data: TransactionIn, session: AsyncSession = Depends(use_session)):
    transaction = await TransactionsSet.create(session, transaction_data)
    transaction_key = await generate_transaction_key(transaction)
    payment_url = get_absolute_uri(f"/payment/{transaction_key}")
    return TransactionCreateResponse(transaction=transaction, payment_url=payment_url)


@router.get('/anonymous/{transaction_key}', response_model=TransactionOutAnonymous)
async def get_transaction_anonymous(transaction_key: str, session: AsyncSession = Depends(use_session)):
    transaction = await TransactionsSet.get_anonymous(session, transaction_key)
    return transaction


@router.get('/', response_model=list[TransactionOut])
async def all_merchant_transactions(merchant_uuid: UUID | None = Query(None),
                                    transactions_set: TransactionsSet = Depends(use_transactions_set),
                                    merchants_set: MerchantsSet = Depends(use_merchants_set)):
    merchant = await merchants_set.get_concrete(merchant_uuid) if merchant_uuid else None
    transactions = await transactions_set.get_all(merchant=merchant)
    return transactions


@router.post('/apply/{transaction_key}', response_model=RedirectResponse)
async def apply_transaction(transaction_key: str,
                            card_info: CardInfo,
                            session: AsyncSession = Depends(use_session)):
    transaction = await TransactionsSet.get_anonymous(session, transaction_key)
    redirect_url = await TransactionsSet.apply_transaction(session, transaction, card_info)
    await delete_transaction_key(transaction_key)
    return RedirectResponse(redirect_url=redirect_url)
