from sqlalchemy import String, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from decimal import Decimal

from app.database.base import Base
from app.database.mixins import TimestampMixin, IdMixin

from app.enums.status import TransactionStatusEnum


class Transaction(IdMixin, TimestampMixin, Base):
    __tablename__ = "transactions"

    transaction_hash: Mapped[str] = mapped_column(String(100), nullable=True)

    currency: Mapped[str] = mapped_column(String(10), default="RUB")
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal(0.00))
    rub_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal(0.00))
    service: Mapped[str] = mapped_column(String(100))
    payment_link: Mapped[str] = mapped_column(String(100), nullable=True)

    status: Mapped[TransactionStatusEnum] = mapped_column(
        Enum(TransactionStatusEnum, name="status_enum"),
        default=TransactionStatusEnum.pending
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True
    )
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, service='{self.service}', user_id={self.user_id})>"