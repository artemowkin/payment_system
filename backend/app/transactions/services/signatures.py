import hmac
import hashlib

from ..schemas import TransactionIn
from ...merchants.schemas import DbMerchant


def validate_signature(transaction_data: TransactionIn, merchant: DbMerchant) -> bool:
    request_signature = transaction_data.signature
    transaction_dict = transaction_data.dict(exclude={'signature'})
    values_string = ''.join([str(transaction_dict[key]) for key in sorted(transaction_dict)])
    generated_signature = hmac.new(merchant.private_key.encode(), values_string.encode(), hashlib.sha256).hexdigest()
    return request_signature == generated_signature
