from app.repositories.service_repository import ServiceRepository
from app.repositories.setting_repository import SettingRepository
from app.repositories.platform_repository import PlatformRepository
from app.repositories.category_repository import CategoryRepository

from app.models.category import Category

from app.dtos.smm_service import ServiceData
from app.utils.helper import convert_to_decimal

from .smm_service import smm_service
from.detector import detect_platform

from app.core.logging import logger

class ServiceUpdater:
    def __init__(
        self,
        repo: ServiceRepository,
        settings_repo: SettingRepository,
        platform_repo: PlatformRepository,
        category_repo: CategoryRepository,
    ):
        self.repo = repo
        self.settings_repo = settings_repo
        self.platform_repo = platform_repo
        self.category_repo = category_repo
        self.smm_service = smm_service

    async def update_all(self):
        services = await self.smm_service.get_services(language="ru")
        settings = await self.settings_repo.get_settings()

        for service in services:
            try:
                category = await self.update_category(service.category)

                price = convert_to_decimal(
                    service.rate + (service.rate / 100 * float(settings.markup_rate))
                )

                await self.update_service(
                    ServiceData(
                        api_service_id=service.service,
                        name=service.name,
                        description=service.description,
                        type=service.type,
                        price=price,
                        original_price=convert_to_decimal(service.rate),
                        min_amount=service.min,
                        max_amount=service.max,
                        time=service.time,
                        category_id=category.id,
                        refill=service.refill,
                        cancel=service.cancel,
                        language="ru"
                    )
                )

            except Exception as ex:
                logger.error(
                    f"Error while updating service [{service.service}] data: {ex}",
                    exc_info=True
                )

    async def update_service(self, service_data: ServiceData):
        service = await self.repo.get_by_api_service_id(
            api_service_id=service_data.api_service_id
        )

        if service:
            return await self.repo.update_service(service, service_data)
        else:
            return await self.repo.create(service_data)

    async def update_category(self, category_name: str) -> Category:
        category = await self.category_repo.get_category_by_name(name=category_name)
        if category:
            return category
        
        platforms = await self.platform_repo.get_all_platforms()
        platform = detect_platform(category_name, platforms)

        if platform is None:
            platform = await self.platform_repo.get_platform_by_name("others")

        return await self.category_repo.create(
            name=category_name,
            platform_id=platform.id
        )