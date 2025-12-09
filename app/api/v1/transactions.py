from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.repositories import get_transaction_repo
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.base import ResponseSchema
from app.schemas.transaction import TransactionOut
from app.schemas.user import UserIn
from app.services.telegram.telegram_service import authorize_user
from app.utils.helper import list_response

router = APIRouter()


@router.post("/", response_model=ResponseSchema[List[TransactionOut]])
async def get_transactions(
        user_in: UserIn,
        repo: TransactionRepository = Depends(get_transaction_repo)
) -> ResponseSchema[List[TransactionOut]]:
    """
    Get all transactions for a user.
    """

    user_data = await authorize_user(user_in.init_data)

    user = await authorize_user(user_data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = await repo.get_by_user_id(user_id=user_data.user_id)

    return list_response(
        data=transactions,
        model=TransactionOut,
        message="Transactions fetched successfully"
    )
