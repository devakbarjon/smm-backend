from aiocryptopay import AioCryptoPay

from app.core.config import settings

crypto = AioCryptoPay(token=settings.CRYPTO_PAY_API_KEY.get_secret_value())


async def create_crypto_invoice(amount: float) -> str:
    invoice = await crypto.create_invoice(
        amount=amount, 
        fiat='USD', 
        currency_type='fiat'
    )

    return invoice.bot_invoice_url