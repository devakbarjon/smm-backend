from pydantic import BaseModel, ConfigDict


class ServiceOut(BaseModel):
    name: str
    description: str
    type: str
    price: float
    min_amount: int
    max_amount: int
    time: str
    category_id: int
    refill: bool = False
    cancel: bool = False
    language: str = "ru"

    model_config = ConfigDict(from_attributes=True)