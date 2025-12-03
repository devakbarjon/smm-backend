from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin, TimestampMixin


class Category(Base, IdMixin, TimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"))
    platform = relationship("Platform", back_populates="categories")

    services = relationship("Service", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"