from datetime import datetime as dt
from uuid import UUID
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, validator

from ..merchants.schemas import DbMerchant, MerchantOut


class Currencies(str, Enum):
    rub = 'RUB'


class TransactionStatuses(str, Enum):
    created = 'created'
    pending = 'pending'
    completed = 'completed'
    failed = 'failed'


class TransactionTypes(str, Enum):
    deposit = 'deposit'


class BaseTransaction(BaseModel):
    type: TransactionTypes = TransactionTypes.deposit
    amount: Decimal
    currency: Currencies = Currencies.rub
    redirect_url: str

    class Config:
        use_enum_values = True


class DbTransaction(BaseTransaction):
    uuid: UUID
    status: TransactionStatuses = TransactionStatuses.created
    merchant: DbMerchant
    card_info: str | None = None
    datetime: dt

    @validator('datetime')
    def datetime_utc(cls, v: dt):
        v = v.astimezone(None)
        return v

    class Config:
        orm_mode = True


class TransactionIn(BaseTransaction):
    merchant_id: UUID
    signature: str
    public_key: str


class TransactionOut(BaseTransaction):
    uuid: UUID
    status: TransactionStatuses = TransactionStatuses.created
    merchant: MerchantOut
    card_info: str | None = None
    datetime: dt


class TransactionOutAnonymous(BaseModel):
    type: TransactionTypes = TransactionTypes.deposit
    amount: Decimal
    currency: Currencies = Currencies.rub


class CardInfo(BaseModel):
    card_code: str = Field(..., regex=r"^\d{4} ?\d{4} ?\d{4} ?\d{4}")
    date: str = Field(..., regex=r"^\d{2}/\d{2}$")
    cvv: str = Field(..., regex=r"^[0-9]{3,4}$")


class RedirectResponse(BaseModel):
    redirect_url: str


class TransactionCreateResponse(BaseModel):
    transaction: TransactionOut
    payment_url: str
