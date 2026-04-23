from decimal import Decimal

from platega import PlategaClient
from pydantic import BaseModel

from app.core.config import settings

platega_client = PlategaClient(
    merchant_id=settings.PLATEGA_MERCHANT_ID,
    secret=settings.PLATEGA_SECRET.get_secret_value(),
)


class PlategaService:

    class CreateTransactionResult(BaseModel):
        transaction_id: str
        payment_link: str | None = None
        raw: dict

    async def create_transaction(
        self,
        amount: float | Decimal,
        currency: str,
        description: str,
        return_url: str,
        failed_url: str,
        payload: str | None = None,
    ) -> CreateTransactionResult:
        # Work around platega-sdk Decimal serialization issue by sending JSON-native numbers.
        amount_number = float(amount)
        request_payload = {
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
            "/v2/transaction/process",
            json=request_payload,
        )

        transaction_id = str(data.get("transactionId") or data.get("id") or "")
        if not transaction_id:
            raise ValueError("Platega response does not include transaction id.")

        payment_link = (
            data.get("redirect")
            or data.get("paymentUrl")
            or data.get("paymentLink")
            or data.get("url")
            or data.get("link")
        )

        return self.CreateTransactionResult(
            transaction_id=transaction_id,
            payment_link=str(payment_link) if payment_link else None,
            raw=data,
        )


platega_service = PlategaService()
