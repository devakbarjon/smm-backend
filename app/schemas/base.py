from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None