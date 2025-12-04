from tonutils.client import ToncenterV3Client
from tonutils.wallet import (
    WalletV4R2,
)

from app.core.config import settings
from app.core.logging import logger

MNEMONIC = settings.TON_WALLET_MNEMONIC.get_secret_value()
API_KEY = settings.TON_CENTER_API_KEY.get_secret_value()

client = ToncenterV3Client(api_key=API_KEY, max_retries=1)

wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(client, MNEMONIC)


class TonService:
    def __init__(self):
        self.wallet = wallet

    async def get_wallet_balance(self):
        try:
            """Get the balance of the wallet."""
            return await self.wallet.get_balance()
        except Exception as e:
            logger.error(f"Failed to get wallet balance: {e}")
            return None

    async def send_transaction(self, to_address: str, amount: int):
        try:
            """Send TON to another address."""
            return await self.wallet.transfer(
                destination=to_address,
                amount=amount
            )
        except Exception as e:
            logger.error(f"Failed to send transaction: {e}")
            return None
    

TonServices = TonService()