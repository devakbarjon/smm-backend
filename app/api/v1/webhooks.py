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
from app.services.telegram.notify import notify_admin, notify

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

    await notify_admin(
        f"Received Stars payment:\n"
        f"User ID: {user.user_id}\n"
        f"Amount: {transaction.amount} {transaction.currency} (~{transaction.rub_amount:.2f} RUB)\n"
        f"Transaction Hash: {transaction.transaction_hash}"
    )

    return {"message": "Webhook processed successfully"}



@router.post("/cryptopay")
async def webhook_cryptopay(
    request: Request,
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Handle incoming CryptoPay payment notifications"""

    payload = await request.json()
    query_params = dict(request.query_params)

    logger.info(f"Received CryptoPay webhook with payload: {payload} and query_params: {query_params}")

    if query_params.get("secret_key") != settings.SECRET_KEY.get_secret_value():
        logger.warning(f"Invalid secret token attempt: {query_params.get('secret_key')}",)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid secret token")

    if payload.get("update_type") != "invoice_paid":
        return {"message": "Event type not handled"}

    invoice_payload = payload.get("payload") or {}
    transaction_id = invoice_payload.get("payload")
    if transaction_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing transaction id in payload")

    transaction = await transaction_repo.get_by_id(int(transaction_id))

    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    user = await user_repo.get_by_id(transaction.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await user_repo.update_balance(
        user=user,
        amount=transaction.rub_amount
    )

    await transaction_repo.update_status(
        transaction_id=transaction.id,
        status=TransactionStatusEnum.success
    )

    await notify_admin(
        f"Received CryptoPay payment:\n"
        f"User ID: {user.user_id}\n"
        f"Amount: {transaction.amount} {transaction.currency} (~{transaction.rub_amount:.2f} RUB)\n"
        f"Transaction ID: {transaction.id}"
    )

    await notify(
        chat_id=user.user_id,
        text=f"Ваш платеж в CryptoPay на сумму {transaction.rub_amount:.2f} RUB был успешно обработан!"
    )

    return {"message": "Webhook processed successfully"}




@router.post("/platega")
async def webhook_platega_payment_status(
    request: Request,
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Handle incoming Platega transaction status callbacks."""

    payload = await request.json()
    merchant_id = request.headers.get("X-MerchantId")
    secret = request.headers.get("X-Secret")

    logger.info(
        "Received Platega callback with payload: %s",
        payload,
    )

    if (
        merchant_id != settings.PLATEGA_MERCHANT_ID
        or secret != settings.PLATEGA_SECRET.get_secret_value()
    ):
        logger.warning(
            "Invalid Platega callback credentials: X-MerchantId=%s",
            merchant_id,
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid callback credentials")

    transaction_id = payload.get("payload")
    if transaction_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing transaction id in payload")

    try:
        transaction_id_int = int(transaction_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction id in payload")

    status_text = str(payload.get("status") or "").strip().upper()
    if status_text not in {"CONFIRMED", "CANCELED", "CHARGEBACKED"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status in payload")

    transaction = await transaction_repo.get_by_id(transaction_id_int)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    user = await user_repo.get_by_id(transaction.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if status_text == "CANCELED":
        transaction.status = TransactionStatusEnum.failed
        transaction.transaction_hash = str(payload.get("id"))
        await transaction_repo.update(transaction)

        return {"message": "Webhook processed successfully"}

    if status_text == "CONFIRMED":
        if transaction.status == TransactionStatusEnum.success:
            return {"message": "Webhook already processed"}

        await user_repo.update_balance(
            user=user,
            amount=transaction.rub_amount
        )

        transaction.status = TransactionStatusEnum.success
        transaction.transaction_hash = str(payload.get("id"))
        await transaction_repo.update(transaction)

        await notify_admin(
            f"Received Platega payment:\n"
            f"User ID: {user.user_id}\n"
            f"Amount: {transaction.amount} {transaction.currency} (~{transaction.rub_amount:.2f} RUB)\n"
            f"Transaction ID: {transaction.id}"
        )

        await notify(
            chat_id=user.user_id,
            text=f"Ваш платеж на сумму {transaction.rub_amount:.2f} RUB был успешно обработан!"
        )
        return {"message": "Webhook processed successfully"}

    if status_text == "CHARGEBACKED" and transaction.status == TransactionStatusEnum.success:
        await user_repo.update_balance(
            user=user,
            amount=-transaction.rub_amount
        )

    transaction.status = TransactionStatusEnum.failed
    transaction.transaction_hash = str(payload.get("id"))
    await transaction_repo.update(transaction)

    await notify_admin(
        f"Platega payment status update: {status_text}\n"
        f"User ID: {user.user_id}\n"
        f"Amount: {transaction.amount} {transaction.currency} (~{transaction.rub_amount:.2f} RUB)\n"
        f"Transaction ID: {transaction.id}"
    )

    return {"message": "Webhook processed successfully"}