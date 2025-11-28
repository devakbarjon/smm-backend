from sqlalchemy import String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from app.db.base import Base
from app.db.mixins import IdMixin, TimestampMixin


class Service(Base, IdMixin, TimestampMixin):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_service_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # Your selling price
    min_amount: Mapped[int] = mapped_column(Integer)
    max_amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(50))  # example: followers, views, likes

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="services")

    orders = relationship("Order", back_populates="service")

    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name}, service_id={self.api_service_id})>"