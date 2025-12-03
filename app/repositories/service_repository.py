from dataclasses import asdict
from .base import BaseRepository

from app.models.service import Service

from app.dtos.smm_service import ServiceData


class ServiceRepository(BaseRepository):
    async def create(
            self, 
            service_data: ServiceData
            ) -> Service:
        
        service_dict = asdict(service_data)
        service = Service(**service_dict)

        return await self.add(service)

    async def get_by_id(self, service_id: int) -> Service | None:
        return await self.get_one(Service, id=service_id)
    
    async def get_by_api_service_id(self, api_service_id: int) -> Service | None:
        return await self.get_one(Service, api_service_id=api_service_id)
    
    async def get_all_services(self) -> list[Service]:
        return await self.get_all(Service)
    
    async def update_service(self, service: Service, service_data: ServiceData):
        service_dict = asdict(service_data)

        return await self.update(service, service_dict)