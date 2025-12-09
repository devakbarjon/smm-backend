from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


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

    async def update(self, instance, **fields):
        for key, value in fields.items():
            setattr(instance, key, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_one(self, model, **filters):
        stmt = select(model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, model, **filters):
        stmt = select(model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_count(self, model, **filters):
        stmt = select(func.count()).select_from(model).filter_by(**filters)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count or 0