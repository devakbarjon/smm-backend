from decimal import ROUND_CEILING, Decimal
import random
import string
from typing import List

from pydantic import TypeAdapter

from app.enums.language import LangEnum
from app.schemas.base import ResponseSchema, T

from app.services.ton.ton_service import TonService


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


def validate_language(lang) -> LangEnum:
    try:
        return LangEnum(lang)
    except Exception:
        return LangEnum.ru


def calculate_cost(price: Decimal, quantity: int) -> Decimal:
    return (price / Decimal(1000)) * quantity


async def calculate_rub_to_stars(amount_rub: Decimal) -> Decimal:
    usd_rate = await TonService.get_usd_rate() # RUB per USD
    stars_rate = Decimal("0.013") # USD per star

    if not usd_rate:
        raise ValueError("Unable to fetch USD to RUB exchange rate")
    
    usd_rate = Decimal(usd_rate)
    amount_rub = Decimal(amount_rub)

    amount_stars = (
        amount_rub / (usd_rate * stars_rate)
    ).to_integral_value(rounding=ROUND_CEILING)

    return amount_stars