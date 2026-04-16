from platega import PlategaClient
from platega.types import PaymentMethod

from app.core.config import settings

platega_client = PlategaClient(
    merchant_id=settings.PLATEGA_MERCHANT_ID,
    secret=settings.PLATEGA_SECRET.get_secret_value(),
)
