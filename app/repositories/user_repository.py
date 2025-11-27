from app.repositories.base import BaseRepository
from app.models.database.user import User

class UserRepository(BaseRepository):

    async def create(self, user_id: int, ref_code: str, ref: str | None = None) -> User:
        user = User(
            user_id=user_id,
            ref_code=ref_code,
            ref=ref
        )
        return await self.add(user)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.get_one(User, user_id=user_id)

    async def get_by_ref_code(self, code: str) -> User | None:
        return await self.get_one(User, ref_code=code)

    async def update_username(self, user_id: int, username: str) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        user.username = username
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_balance(self, user_id: int, amount: float) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        user.balance += amount
        await self.session.commit()
        await self.session.refresh(user)
        return user