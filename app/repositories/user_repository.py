from sqlalchemy.orm.attributes import flag_modified

from app.repositories.base import BaseRepository
from app.models.user import User

from app.utils.helper import random_string


class UserRepository(BaseRepository):

    async def create(self, user_id: int, ref_id: int | None, lang: str) -> User:
        ref_code = random_string(10)

        user = User(
            user_id=user_id,
            ref_code=ref_code,
            ref_id=ref_id,
            lang=lang
        )
        
        return await self.add(user)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.get_one(User, user_id=user_id)

    async def get_by_ref_code(self, code: str) -> User | None:
        return await self.get_one(User, ref_code=code)

    async def add_favorite_service(self, user_id: int, service_id: int) -> list:
        user = await self.get_by_id(user_id)

        if service_id not in user.favorite_services:
            user.favorite_services.append(service_id)
            flag_modified(user, "favorite_services")
            await self.update(user)

        return user.favorite_services