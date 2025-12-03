from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_order_repo(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def get_service_repo(db: AsyncSession = Depends(get_db)) -> ServiceRepository:
    return ServiceRepository(db)


async def get_setting_repo(db: AsyncSession = Depends(get_db)) -> SettingRepository:
    return SettingRepository(db)