from dataclasses import dataclass


@dataclass
class ServiceData:
    service: str
    name: str
    description: str
    type: str
    price: float
    original_price: float
    min_amount: int
    max_amount: int
    time: str
    refill: bool = False
    cancel: bool = False
    language: str = "ru"