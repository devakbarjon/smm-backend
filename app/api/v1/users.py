from fastapi import APIRouter, Depends, HTTPException

from app.schemas.base import ResponseSchema
from app.schemas.user import UserIn, UserOut, UserFavoriteIn, UserFavoriteOut, UserLanguageIn, UserLanguageOut

from app.repositories.user_repository import UserRepository
from app.dependencies.repositories import get_user_repo

from app.services.telegram.telegram_service import authorize_user

from app.utils.helper import response

router = APIRouter()


@router.post("/", response_model=ResponseSchema[UserOut])
async def get_user(
        user_in: UserIn,
        user_repo: UserRepository = Depends(get_user_repo)
) -> ResponseSchema[UserOut]:
    """
    Create or get a user.
    """

    user_data = await authorize_user(user_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:

        if user_in.start_param:
            ref_user = await user_repo.get_by_ref_code(user_in.start_param)
            ref_id = ref_user.user_id if ref_user else None
        else:
            ref_id = None

        user = await user_repo.create(
            user_id=user_data.user_id,
            ref_id=ref_id,
            lang=user_data.lang_code
        )

    user.ref_count = await user_repo.get_ref_count(user_id=user.user_id)

    return response(
        data=user,
        model=UserOut,
        message="User fetched successfully"
    )


@router.post("/favorites", response_model=ResponseSchema[UserFavoriteOut])
async def get_favorites(
        user_in: UserIn,
        user_repo: UserRepository = Depends(get_user_repo)
):
    """
    Get a favorite services of user.
    """

    user_data = await authorize_user(user_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return response(
        data=await user.favorites,
        model=UserFavoriteOut,
        message="Favorites fetched successfully"
    )


@router.post("/add_favorite", response_model=ResponseSchema[UserFavoriteOut])
async def add_favorite_service(
        favorite_in: UserFavoriteIn,
        user_repo: UserRepository = Depends(get_user_repo)
) -> ResponseSchema[UserFavoriteOut]:
    """
    Add a favorite service.
    """

    user_data = await authorize_user(init_data=favorite_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    user_services = await user_repo.update_favorite_service(
        user_id=user.user_id,
        service_id=favorite_in.service_id
    )

    return response(
        data=user_services,
        model=UserFavoriteOut,
        message="Service added to favorites successfully"
    )


@router.delete("/delete_favorite", response_model=ResponseSchema[UserFavoriteOut])
async def delete_favorite_service(
    favorite_in: UserFavoriteIn,
    user_repo: UserRepository = Depends(get_user_repo)
) -> ResponseSchema[UserFavoriteOut]:
    """
    Delete a favorite service.
    """

    user_data = await authorize_user(init_data=favorite_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    user_services = await user_repo.update_favorite_service(
        user_id=user.user_id,
        service_id=favorite_in.service_id,
        is_delete=True
    )

    return response(
        data=user_services,
        model=UserFavoriteOut,
        message="Service deleted from favorites successfully"
    )


@router.post("/language", response_model=ResponseSchema[UserLanguageOut])
async def change_language(
        language_in: UserLanguageIn,
        user_repo: UserRepository = Depends(get_user_repo)
) -> ResponseSchema[UserLanguageOut]:
    """
    Change user language.
    """

    user_data = await authorize_user(init_data=language_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    if language_in.lang not in ["ru", "en"]:
        raise HTTPException(status_code=400, detail="Invalid language!")

    user.lang = language_in.lang
    await user_repo.update(user)

    return response(
        data=user.lang,
        model=UserLanguageOut,
        message="Language updated successfully"
    )