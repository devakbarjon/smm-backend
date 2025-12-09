from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from .telegram import TMAInitData

from app.enums.language import LangEnum


class UserIn(TMAInitData):
    start_param: str | int | None = None


class UserOut(BaseModel):
    user_id: int
    lang: LangEnum
    balance: Decimal
    ref_code: str
    ref_count: int
    ref_income: Decimal

    model_config = ConfigDict(from_attributes=True)


class UserFavoriteIn(TMAInitData):
    service_id: int


class UserFavoriteOut(BaseModel):
    favorite_services: list[int]


class UserLanguageIn(TMAInitData):
    lang: LangEnum


class UserLanguageOut(BaseModel):
    lang: LangEnum