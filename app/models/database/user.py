from sqlalchemy import String, DateTime, BigInteger, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from decimal import Decimal

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)

    lang: Mapped[str | None] = mapped_column(String(10), nullable=True)

    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    ref: Mapped[str | None] = mapped_column(String, nullable=True)
    ref_code: Mapped[str] = mapped_column(String, unique=True, index=True)
    ref_income: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)


    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.user_id}, username={self.username})>"