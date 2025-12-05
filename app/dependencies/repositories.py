from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository
from app.repositories.platform_repository import PlatformRepository
from app.repositories.category_repository import CategoryRepository


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_order_repo(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def get_service_repo(db: AsyncSession = Depends(get_db)) -> ServiceRepository:
    return ServiceRepository(db)


async def get_setting_repo(db: AsyncSession = Depends(get_db)) -> SettingRepository:
    return SettingRepository(db)


async def get_platform_repo(db: AsyncSession = Depends(get_db)) -> PlatformRepository:
    return PlatformRepository(db)


async def get_category_repo(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)