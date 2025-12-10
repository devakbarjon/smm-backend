from decimal import Decimal

from sqlalchemy import String, Integer, ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin, TimestampMixin


class Order(IdMixin, Base, TimestampMixin):
    __tablename__ = "orders"

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    link: Mapped[str] = mapped_column(String(500), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)

    is_done: Mapped[bool] = mapped_column(default=False)
    parent_order_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    service = relationship("Service", back_populates="orders")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True
    )
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, service_id={self.service_id}, status={self.status})>"