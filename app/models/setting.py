from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin


class Setting(IdMixin, Base):
    __tablename__ = "settings"

    markup_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    ton_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    min_deposit_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))