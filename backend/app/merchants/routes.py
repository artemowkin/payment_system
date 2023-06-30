from uuid import UUID

from fastapi import APIRouter, Depends

from .schemas import MerchantOut, MerchantIn
from .services.merchants import MerchantsSet
from .dependencies import use_merchants_set


router = APIRouter()


@router.post('/', response_model=MerchantOut)
async def create_merchant(merchant_data: MerchantIn, merchants_set: MerchantsSet = Depends(use_merchants_set)):
    db_merchant = await merchants_set.create(merchant_data)
    return MerchantOut(**db_merchant.dict())


@router.get('/', response_model=list[MerchantOut])
async def all_user_merchants(merchants_set: MerchantsSet = Depends(use_merchants_set)):
    db_merchants = await merchants_set.all()
    return [MerchantOut(**db_merchant.dict()) for db_merchant in db_merchants]


@router.put('/{merchant_uuid}/tokens/', response_model=MerchantOut)
async def regenerate_tokens(merchant_uuid: UUID, merchants_set: MerchantsSet = Depends(use_merchants_set)):
    db_merchant = await merchants_set.get_concrete(merchant_uuid)
    new_merchant = await merchants_set.regenerate_tokens(db_merchant)
    return MerchantOut(**new_merchant.dict())


@router.delete('/{merchant_uuid}/', status_code=204)
async def block_merchant(merchant_uuid: UUID, merchants_set: MerchantsSet = Depends(use_merchants_set)):
    db_merchant = await merchants_set.get_concrete(merchant_uuid)
    await merchants_set.block(db_merchant)
