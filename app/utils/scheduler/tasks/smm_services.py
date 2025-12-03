from app.database.base import AsyncSessionLocal

from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository

from app.services.smm.updater import ServiceUpdater


async def update_service_data():
    async with AsyncSessionLocal() as session:
        repo = ServiceRepository(session)
        settings_repo = SettingRepository(session=session)
        updater = ServiceUpdater(
            repo=repo,
            settings_repo=settings_repo
        )

        await updater.update_all()