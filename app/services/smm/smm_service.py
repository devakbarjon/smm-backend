from . base import smm_api

from soc_proof.models import Service, OrderStatus, AccountBalance


class SMMService:
    def __init__(self):
        self.smm_api = smm_api

    async def create_order(self, service_id: int, link: str, quantity: int) -> str | None:

        order_id = await self.smm_api.add_order(
            service_id=service_id,
            link=link,
            quantity=quantity
        )

        return order_id
    
    async def get_order_status(self, order_id: int) -> OrderStatus:
        order_status = await self.smm_api.get_order_status(order_id=order_id)

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