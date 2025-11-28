from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import IdMixin, TimestampMixin


class Platform(Base, IdMixin, TimestampMixin):
    __tablename__ = "platforms"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    categories = relationship("Category", back_populates="platform")

    def __repr__(self):
        return f"<Platform(id={self.id}, name={self.name})>"