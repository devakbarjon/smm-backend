import httpx

from app.core.config import settings
from app.core.logging import logger


TONAPI_BASE = "https://tonapi.io/v2"


async def fetch_transaction_details(tx_hash: str):
    try:
        """Fetch full transaction data from TonAPI."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{TONAPI_BASE}/blockchain/transactions/{tx_hash}",
                headers={"Authorization": f"Bearer {settings.tonapi_key}"}
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as e:
        logger.error(f"Error fetching transaction details: {e}")
        return None