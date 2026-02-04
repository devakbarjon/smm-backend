import httpx

from tonutils.client import ToncenterV3Client
from tonutils.wallet import (
    WalletV4R2,
)

from app.core.config import settings
from app.core.logging import logger

MNEMONIC = settings.TON_WALLET_MNEMONIC.get_secret_value()
API_KEY = settings.TON_CENTER_API_KEY.get_secret_value()
TONAPI_BASE = "https://tonapi.io/v2"

client = ToncenterV3Client(api_key=API_KEY, max_retries=1)

wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, MNEMONIC)


class TonServiceClass:
    def __init__(self):
        self.wallet = wallet

    async def get_wallet_balance(self):
        try:
            """Get the balance of the wallet."""
            return await self.wallet.get_balance()
        except Exception as e:
            logger.error(f"Failed to get wallet balance: {e}")
            return None
        
    async def get_transaction(self, tx_hash: str) -> dict | None:
        try:
            """Fetch full transaction data from TonAPI."""
            async with httpx.AsyncClient() as client:
                url = f"{TONAPI_BASE}/blockchain/transactions/{tx_hash}"
                headers = {"Authorization": f"Bearer {settings.TON_API_KEY.get_secret_value()}"}

                resp = await client.get(
                    url,
                    headers=headers
                )
                resp.raise_for_status()
                
                data = resp.json()

                in_msg = data.get("in_msg", {})
                return in_msg
        except httpx.HTTPError as e:
            logger.error(f"Error fetching transaction details: {e}")
            return None
        
    async def get_ton_rate(self) -> float | None:
        try:
            """Fetch current TON to RUB exchange rate."""
            async with httpx.AsyncClient() as client:
                url = f"{TONAPI_BASE}/rates"
                headers = {"Authorization": f"Bearer {settings.TON_API_KEY.get_secret_value()}"}
                params = {
                    "tokens": "ton",
                    "currencies": "rub"
                }

                resp = await client.get(
                    url,
                    headers=headers,
                    params=params
                )

                resp.raise_for_status()
                data = resp.json()

                rate = data.get("rates", {}).get("TON", {}).get("prices", {}).get("RUB", None)
                return rate
        except httpx.HTTPError as e:
            logger.error(f"Error fetching TON exchange rate: {e}")
            return None

    async def get_usd_rate(self) -> float | None:
        try:
            """Fetch current USD to RUB exchange rate."""
            async with httpx.AsyncClient() as client:
                url = f"{TONAPI_BASE}/rates"
                headers = {"Authorization": f"Bearer {settings.TON_API_KEY.get_secret_value()}"}
                params = {
                    "tokens": "usd",
                    "currencies": "rub"
                }

                resp = await client.get(
                    url,
                    headers=headers,
                    params=params
                )

                resp.raise_for_status()
                data = resp.json()

                rate = data.get("rates", {}).get("USD", {}).get("prices", {}).get("RUB", None)
                return rate
        except httpx.HTTPError as e:
            logger.error(f"Error fetching USD to RUB exchange rate: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching USD to RUB exchange rate: {e}")
            return None
    

TonService = TonServiceClass()