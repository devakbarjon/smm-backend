from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.config import settings
from app.dependencies.repositories import get_transaction_repo, get_user_repo
from app.enums.status import TransactionStatusEnum
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.webhook import WebhookIn

router = APIRouter()


@router.post("/stars")
async def webhook_stars(
    payload: WebhookIn,
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    if payload.secret_key != settings.SECRET_KEY.get_secret_value():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret token")

    transaction = await transaction_repo.get_by_id(payload.transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction.amount != payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")

    user = await user_repo.get_by_id(transaction.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.balance += transaction.rub_amount
    await user_repo.update(user)

    transaction.status = TransactionStatusEnum.success
    transaction.transaction_hash = payload.transaction_hash
    await transaction_repo.update(transaction)

    return {"message": "Webhook processed successfully"}
