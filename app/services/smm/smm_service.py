from . base import smm_api

from soc_proof.models import Service, OrderStatus, AccountBalance
from soc_proof.errors import NotEnoughFundsError

from app.core.logging import logger

from app.services.telegram.notify import notify_admin


class SMMService:
    def __init__(self):
        self.smm_api = smm_api

    async def create_order(self, service_id: int, link: str, quantity: int) -> str | None:

        try:
            order_id = await self.smm_api.add_order(
                service=service_id,
                link=link,
                quantity=quantity
            )

            return order_id
        except NotEnoughFundsError:
            balance = await self.get_balance()

            await notify_admin(
                f"Failed to create SMM order due to insufficient funds.\n"
                f"Current balance: {balance.balance} {balance.currency}\n"
                f"Attempted order - Service ID: {service_id}, Link: {link}, Quantity: {quantity}"
            )

            logger.error("Not enough funds to create SMM order.")
            return None
        except Exception as e:
            logger.error(f"Error creating SMM order: {e}")
            return None
    
    async def get_order_status(self, orders: str | list) -> OrderStatus:
        order_status = await self.smm_api.get_status(orders=orders)

        return order_status
    
    async def get_services(self, language: str = "en") -> list[Service]:
        services = await self.smm_api.load_services(language=language)

        return services
    
    async def get_single_service(self, service_id: int) -> Service:
        service = await self.smm_api.get_service(service_id=service_id)

        return service

    async def get_balance(self) -> AccountBalance:
        balance = await self.smm_api.get_balance()

        return balance


smm_service = SMMService()