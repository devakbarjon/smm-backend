from sqlalchemy import Column, DateTime, Integer, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped


class IdMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)