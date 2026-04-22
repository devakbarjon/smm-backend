from decimal import Decimal

from platega import PlategaClient
from platega.models import CreateTransactionResponse
from platega.types import PaymentMethod

from app.core.config import settings

platega_client = PlategaClient(
    merchant_id=settings.PLATEGA_MERCHANT_ID,
    secret=settings.PLATEGA_SECRET.get_secret_value(),
)


class PlategaService:
    async def create_transaction(
        self,
        payment_method: PaymentMethod,
        amount: float | Decimal,
        currency: str,
        description: str,
        return_url: str,
        failed_url: str,
        payload: str | None = None,
    ) -> CreateTransactionResponse:
        # Work around platega-sdk Decimal serialization issue by sending JSON-native numbers.
        amount_number = float(amount)
        request_payload = {
            "paymentMethod": int(payment_method),
            "paymentDetails": {
                "amount": amount_number,
                "currency": currency,
            },
            "description": description,
            "return": return_url,
            "failedUrl": failed_url,
            "payload": payload,
        }

        data = await platega_client._request(
            "POST",
            "/transaction/process",
            json=request_payload,
        )
        return CreateTransactionResponse(**data)


platega_service = PlategaService()
