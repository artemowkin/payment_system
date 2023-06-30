from uuid import uuid4

from sqlalchemy.types import UUID, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ..project.db import Base


class User(Base):
    __tablename__ = 'users'

    uuid = mapped_column(UUID, primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))
    middle_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    email: Mapped[str] = mapped_column(String(length=200), unique=True)
    password: Mapped[str] = mapped_column(String(length=500))
