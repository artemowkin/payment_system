from uuid import uuid4

from sqlalchemy.types import UUID, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint

from ..project.db import Base
from ..users.models import User


class Merchant(Base):
    __tablename__ = 'merchants'
    __table_args__ = (
        UniqueConstraint('user_id', 'slug', name='slug_user_uc'),
    )

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(length=100))
    public_key: Mapped[str] = mapped_column(String(length=500))
    private_key: Mapped[str] = mapped_column(String(length=500))
    user_id: Mapped[str] = mapped_column(ForeignKey(User.uuid, ondelete='CASCADE'))
    user: Mapped[User] = relationship()
    blocked: Mapped[bool] = mapped_column(default=False)
