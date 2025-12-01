from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseSchema(GenericModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None