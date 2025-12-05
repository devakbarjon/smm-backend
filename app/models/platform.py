from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin, TimestampMixin


class Platform(IdMixin, Base, TimestampMixin):
    __tablename__ = "platforms"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    keywords: Mapped[str] = mapped_column(String, default="")  # comma-separated list

    categories = relationship("Category", back_populates="platform")

    def __repr__(self):
        return f"<Platform(id={self.id}, name={self.name})>"