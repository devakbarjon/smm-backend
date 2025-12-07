from pydantic import BaseModel

from .telegram import TMAInitData


class DepositIn(TMAInitData):
    amount: int  # In rub