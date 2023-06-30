from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.types import String, DECIMAL, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..merchants.models import Merchant
from ..project.db import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    status: Mapped[str] = mapped_column(String(length=20))
    type: Mapped[str] = mapped_column(String(length=10))
    merchant_id: Mapped[str] = mapped_column(ForeignKey(Merchant.uuid, ondelete='CASCADE'))
    merchant: Mapped[Merchant] = relationship()
    amount = mapped_column(DECIMAL(20, 2))
    currency: Mapped[str] = mapped_column(String(length=10))
    redirect_url: Mapped[str] = mapped_column(String(length=500))
    card_info: Mapped[str] = mapped_column(String(length=4), nullable=True)
    datetime = mapped_column(DateTime(), default=datetime.utcnow)
