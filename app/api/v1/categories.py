from typing import List
from fastapi import APIRouter, Depends

from app.schemas.base import ResponseSchema
from app.schemas.category import CategoryOut

from app.dependencies.repositories import get_category_repo

from app.repositories.category_repository import CategoryRepository
from app.utils.helper import list_response

router = APIRouter()


@router.get("/{platform_id}")
async def get_categories_by_platform_id(
        platform_id: int,
        repo: CategoryRepository = Depends(get_category_repo)
) -> ResponseSchema[List[CategoryOut]]:
    services = await repo.get_categories_by_platform(platform_id=platform_id)

    return list_response(
        data=services,
        model=CategoryOut
    )