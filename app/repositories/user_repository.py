from app.repositories.base import BaseRepository
from app.models.user import User

from app.utils.helper import random_string

class UserRepository(BaseRepository):

    async def create(self, user_id: int, ref_id: int) -> User:
        ref_code = random_string(10)

        user = User(
            user_id=user_id,
            ref_code=ref_code,
            ref_id=ref_id
        )
        
        return await self.add(user)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.get_one(User, user_id=user_id)

    async def get_by_ref_code(self, code: str) -> User | None:
        return await self.get_one(User, ref_code=code)