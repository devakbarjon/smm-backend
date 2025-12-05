from sqlalchemy import String, Integer, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from app.database.base import Base
from app.database.mixins import IdMixin, TimestampMixin

class Service(IdMixin, Base, TimestampMixin):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_service_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2)) # Our price per 1000 units
    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2)) # Real price from SMM panel per 1000 units
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), default="ru") # Detail's language
    time : Mapped[str | None] = mapped_column(String(100), nullable=True) # Approximate time to complete the order
    refill: Mapped[bool] = mapped_column(default=False)
    cancel: Mapped[bool] = mapped_column(default=False)
    min_amount: Mapped[int] = mapped_column(Integer)
    max_amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(50))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="services")

    orders = relationship("Order", back_populates="service")

    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name}, service_id={self.api_service_id})>"