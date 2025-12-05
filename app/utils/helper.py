from decimal import Decimal
from random import random
import string
from typing import List

from pydantic import TypeAdapter

from app.schemas.base import ResponseSchema, T


def random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string of given length."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def convert_to_decimal(value: str | float | int):
    return Decimal(value)


def list_response(data: list[T], model: type[T], message: str = None):
    adapter = TypeAdapter(List[model])
    validated = adapter.validate_python(data)
    return ResponseSchema[List[T]](data=validated, message=message)


def response(data: T, model: type[T], message: str = None):
    adapter = TypeAdapter(model)
    validated = adapter.validate_python(data)
    return ResponseSchema[T](data=validated, message=message)