from pydantic import BaseModel, ConfigDict
from .telegram import TMAInitData


class UserIn(TMAInitData):
    start_param: str | int | None = None


class UserOut(BaseModel):
    user_id: int
    lang: str | None
    balance: float
    ref_code: str
    ref_income: float

    model_config = ConfigDict(from_attributes=True)