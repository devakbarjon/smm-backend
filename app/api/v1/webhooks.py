from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status

from app.core.config import settings
from app.core.logging import logger

from app.dependencies.repositories import get_transaction_repo, get_user_repo

from app.enums.status import TransactionStatusEnum

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository

from app.schemas.webhook import WebhookIn

from app.services.ton.ton_service import TonService
from app.services.telegram.notify import notify_admin

router = APIRouter()


@router.post("/stars")
async def webhook_stars(
    payload: WebhookIn,
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Handle incoming Stars payment notifications"""

    if payload.secret_key != settings.SECRET_KEY.get_secret_value():
        logger.warning(f"Invalid secret token attempt: {payload.secret_key}",)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret token")

    transaction = await transaction_repo.get_by_id(payload.transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    if transaction.amount != payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount")

    user = await user_repo.get_by_id(transaction.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await user_repo.update_balance(
        user=user,
        amount=transaction.rub_amount
    )

    transaction.status = TransactionStatusEnum.success
    transaction.transaction_hash = payload.transaction_hash
    await transaction_repo.update(transaction)

    return {"message": "Webhook processed successfully"}



@router.post("/ton")
async def webhook_ton(
    request: Request,
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo)
):
    """Handle incoming TON blockchain transactions"""
    
    payload = await request.json()
    query_params = dict(request.query_params)
    event = payload.get("event") or payload.get("event_type")

    logger.info(f"Received TON webhook event: {event} with payload: {payload} and query_params: {query_params}")

    if event != "account_tx":
        return {"message": "Event type not handled"}
    
    tx_hash = payload.get("tx_hash")
    if not tx_hash:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing transaction hash")
    
    data = await TonService.get_transaction(tx_hash)
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing data in payload")
    
    rate = await TonService.get_ton_rate()
    if not rate:
        logger.error("Failed to fetch TON exchange rate")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch TON exchange rate")
    
    amount = int(data.get("value", 0)) / 1e9 
    amount_rub = amount * rate
    sender = data.get("source", {}).get("address", "")
    comment = data.get("decoded_body", "")

    if not comment.isdigit():
        logger.error(f"Invalid comment format: {comment}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid comment format")
    
    if not sender or amount <= 0:
        logger.error(f"Invalid sender or amount: sender={sender}, amount={amount}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sender or amount")
    

    user = await user_repo.get_by_id(int(comment))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await user_repo.update_balance(
        user=user,
        amount=amount_rub
    )

    await transaction_repo.create(
        user_id=user.user_id,
        amount=amount,
        rub_amount=amount_rub,
        service="ton_wallet",
        status=TransactionStatusEnum.success,
        currency="TON",
        transaction_hash=tx_hash
    )

    await notify_admin(
        f"Received TON payment:\n"
        f"User ID: {user.user_id}\n"
        f"Amount: {amount} TON (~{amount_rub:.2f} RUB)\n"
        f"Sender: {sender}\n"
        f"Transaction Hash: {tx_hash}"
    )

    return {"status": "ok"}