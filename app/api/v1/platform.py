from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.base import ResponseSchema
from app.schemas.service import ServiceOut

from app.dependencies.repositories import get_service_repo

from app.repositories.service_repository import ServiceRepository
from app.utils.helper import list_response

router = APIRouter()


@router.get("/{category_id}")
async def get_services_by_catgery_id(
        category_id: int,
        repo: ServiceRepository = Depends(get_service_repo)
) -> ResponseSchema[List[ServiceOut]]:
    services = await repo.get_services_by_category_id(category_id=category_id)

    return list_response(
        data=services,
        model=ServiceOut
    )