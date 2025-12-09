from pydantic import BaseModel, ConfigDict
from .telegram import TMAInitData


class OrderIn(TMAInitData):
    service_id: int
    link: str
    quantity: int


class OrderOut(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderStatusIn(TMAInitData):
    order_id: int


class OrderStatusOut(BaseModel):
    id: int
    quantity: int
    link: str
    service_id: int
    charge: float
    status: str
    remains: int


class OrderStatusListOut(BaseModel):
    orders: list[OrderStatusOut]

    model_config = ConfigDict(from_attributes=True)