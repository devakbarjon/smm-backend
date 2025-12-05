from fastapi import APIRouter, Depends, HTTPException

from app.schemas.base import ResponseSchema
from app.schemas.user import UserIn, UserOut

from app.repositories.user_repository import UserRepository
from app.dependencies.repositories import get_user_repo

from app.services.telegram.telegram_service import authorize_user

from app.utils.helper import response

router = APIRouter()


@router.post("/")
async def user_me(
    user_in: UserIn,
    user_repo: UserRepository = Depends(get_user_repo),
) -> ResponseSchema[UserOut]:
    """
    Create or get a user.
    """
    
    user_data = await authorize_user(user_in.init_data)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid init_data signature!")

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:

        if user_in.start_param:
            ref_user = await user_repo.get_by_ref_code(user_in.start_param)
            ref_id = ref_user.user_id if ref_user else None
        else:
            ref_id = None

        user = await user_repo.create(
            user_id=user_data.user_id,
            ref_id=ref_id
        )

    return response(
        data=user,
        model=UserOut
    )
