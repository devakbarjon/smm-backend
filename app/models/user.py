from sqlalchemy import String, BigInteger, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from decimal import Decimal

from app.db.base import Base
from app.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)

    lang: Mapped[str | None] = mapped_column(String(10), nullable=True)

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    ref: Mapped[str | None] = mapped_column(String, nullable=True)
    ref_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    ref_income: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"