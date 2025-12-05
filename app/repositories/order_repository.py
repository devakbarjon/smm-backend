from app.repositories.base import BaseRepository
from app.models.order import Order


class OrderRepository(BaseRepository):
    async def create(self, user_id: int, service_id: int, quantity: int, link: str) -> Order:
        order = Order(
            user_id=user_id,
            service_id=service_id,
            quantity=quantity,
            link=link
        )
        return await self.add(order)

    async def get_by_id(self, order_id: int) -> Order | None:
        return await self.get_one(Order, id=order_id)
    
    async def get_by_user_and_order_id(self, user_id: int, order_id: int) -> Order | None:
        return await self.get_one(Order, id=order_id, user_id=user_id)
    
    async def get_by_user_id(self, user_id: int) -> list[Order]:
        return await self.get_all(Order, user_id=user_id)

    async def mark_as_done(self, order_id: int) -> Order | None:
        order = await self.get_by_id(order_id)
        if not order:
            return None

        return await self.update(Order, is_done=True)