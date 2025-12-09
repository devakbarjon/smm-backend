from typing import List
from fastapi import APIRouter, Depends

from app.schemas.base import ResponseSchema
from app.schemas.platform import PlatformOut

from app.dependencies.repositories import get_platform_repo

from app.repositories.platform_repository import PlatformRepository
from app.utils.helper import list_response

router = APIRouter()


@router.get("/")
async def get_all_platforms(
        repo: PlatformRepository = Depends(get_platform_repo)
) -> ResponseSchema[List[PlatformOut]]:
    """
    Get all platforms.
    """
    platforms = await repo.get_all_platforms()

    return list_response(
        data=platforms,
        model=PlatformOut,
        message="All platforms fetched successfully."
    )
