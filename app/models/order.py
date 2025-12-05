from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin, TimestampMixin


class Order(IdMixin, Base, TimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    link: Mapped[str] = mapped_column(String(500), nullable=False)

    is_done: Mapped[bool] = mapped_column(default=False)
    order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user = relationship("User", back_populates="orders")
    service = relationship("Service", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, service_id={self.service_id}, status={self.status})>"