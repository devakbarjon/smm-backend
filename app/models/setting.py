from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import IdMixin


class Setting(Base, IdMixin):
    __tablename__ = "settings"

    markup_rate: Mapped[float] = mapped_column(Numeric(10, 2))