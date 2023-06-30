from uuid import UUID

from pydantic import BaseModel


class KeysPair(BaseModel):
    public_key: str
    private_key: str


class BaseMerchant(BaseModel):
    slug: str


class DbMerchant(BaseMerchant):
    uuid: UUID
    public_key: str
    private_key: str
    user_id: UUID

    class Config:
        orm_mode = True


class MerchantIn(BaseMerchant):
    ...


class MerchantOut(BaseMerchant):
    uuid: UUID
    public_key: str
    private_key: str
