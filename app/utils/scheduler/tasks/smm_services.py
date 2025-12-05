from app.database.base import AsyncSessionLocal

from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.platform_repository import PlatformRepository

from app.services.smm.updater import ServiceUpdater


async def update_service_data():
    async with AsyncSessionLocal() as session:
        repo = ServiceRepository(session)
        settings_repo = SettingRepository(session=session)
        category_repo = CategoryRepository(session=session)
        platform_repo = PlatformRepository(session=session)

        updater = ServiceUpdater(
            repo=repo,
            settings_repo=settings_repo,
            category_repo=category_repo,
            platform_repo=platform_repo
        )

        await updater.update_all()