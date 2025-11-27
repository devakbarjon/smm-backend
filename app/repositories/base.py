from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, instance):
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance):
        await self.session.delete(instance)
        await self.session.commit()

    async def get_one(self, model, **filters):
        stmt = select(model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, model, **filters):
        stmt = select(model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()