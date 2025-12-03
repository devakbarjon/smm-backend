from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository

from app.dtos.smm_service import ServiceData

from .smm_service import smm_service

class ServiceUpdater:
    def __init__(self, repo: ServiceRepository, settings_repo: SettingRepository):
        self.repo = repo
        self.settings_repo = settings_repo
        self.smm_service = smm_service

    async def update_all(self):
        services = await self.smm_service.get_services(language="ru")
        settings = await self.settings_repo.get_settings()

        for service in services:
            await self.update_service(
                ServiceData(
                    service=service.service,
                    name=service.name,
                    description=service.description,
                    type=service.type,
                    price=service.rate * (service.rate / 100 * settings.markup_rate),
                    orginal_price=service.rate,
                    min_amount=service.min,
                    max_amount=service.max,
                    time=service.time,
                    refill=service.refill,
                    cancel=service.cancel,
                    language="ru"
                )
            )

    async def update_service(self, service_data: ServiceData):
        service_in_db = await self.repo.get_by_api_service_id(api_service_id=service_data.service)
        if service_in_db:
            await self.repo.update_service(service_in_db, service_data)
        else:
            await self.repo.create(service_data)