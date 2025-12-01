from pydantic import BaseModel, ConfigDict
from .telegram import TMAInitData


class OrderIn(TMAInitData):
    service_id: int
    link: str
    quantity: int


class OrderOut(BaseModel):
    order_id: str

    model_config = ConfigDict(from_attributes=True)


class OrderStatusIn(TMAInitData):
    order_id: str


class OrderStatusOut(BaseModel):
    order_id: str
    charge: float
    status: str
    remains: int

    model_config = ConfigDict(from_attributes=True)


class OrderStatusListOut(BaseModel):
    orders: list[OrderStatusOut]

    model_config = ConfigDict(from_attributes=True)