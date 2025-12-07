from sqlalchemy import String, BigInteger, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from decimal import Decimal

from app.database.base import Base
from app.database.mixins import TimestampMixin

from app.enums.language import LangEnum


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    full_name: Mapped[str | None] = mapped_column(String, nullable=False)
    username: Mapped[str | None] = mapped_column(String, nullable=True)

    lang: Mapped[LangEnum | None] = mapped_column(
        Enum(LangEnum, name="lang_enum"),
        default=LangEnum.ru
    )

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    ref_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id"),
        nullable=True
    )
    referrer = relationship(
        "User",
        remote_side=[user_id],
        back_populates="referrals"
    )
    referrals = relationship(
        "User",
        back_populates="referrer",
        cascade="all, delete-orphan"
    )
    ref_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    ref_income: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal(0.00))

    favorite_services: Mapped[list[int]] = mapped_column(ARRAY(BigInteger), default=list)

    orders = relationship(
        "Order",
        back_populates="user",
        cascade="save-update, merge",
        passive_deletes=True
    )

    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="save-update, merge",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"