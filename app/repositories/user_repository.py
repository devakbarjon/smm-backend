from decimal import Decimal

from sqlalchemy.orm.attributes import flag_modified

from app.repositories.base import BaseRepository
from app.models.user import User
from app.enums.language import LangEnum
from app.utils.helper import random_string


class UserRepository(BaseRepository):

    async def create(
            self,
            user_id: int,
            ref_id: int | None,
            lang: str,
            full_name: str,
            username: str | None = None
    ) -> User:
        ref_code = random_string(10)

        user = User(
            user_id=user_id,
            ref_code=ref_code,
            ref_id=ref_id,
            lang=lang,
            full_name=full_name,
            username=username
        )
        
        return await self.add(user)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.get_one(User, user_id=user_id)

    async def get_by_ref_code(self, code: str) -> User | None:
        return await self.get_one(User, ref_code=code)

    async def update_favorite_service(
            self, user_id: int,
            service_id: int,
            is_delete: bool = False
    ) -> list:
        user = await self.get_by_id(user_id)

        if service_id not in user.favorite_services and not is_delete:
            user.favorite_services.append(service_id)

        if service_id in user.favorite_services and is_delete:
            user.favorite_services.remove(service_id)

        flag_modified(user, "favorite_services")
        await self.update(user)

        return user.favorite_services

    async def get_ref_count(self, user_id: int) -> int:
        return await self.get_count(User, ref_id=user_id)
    
    async def update_balance(self, user: User, amount: float | Decimal) -> User:
        amount = Decimal(amount)
        user.balance += amount
        return await self.update(user)
    
    async def update_language(self, user: User, lang: LangEnum) -> User:
        user.lang = lang
        return await self.update(user)