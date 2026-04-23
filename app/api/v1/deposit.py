from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from starlette import status

from app.core.config import settings

from app.schemas.base import ResponseSchema
from app.schemas.deposit import DepositIn
from app.schemas.transaction import TransactionOut

from app.dependencies.repositories import get_transaction_repo, get_user_repo

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository

from app.services.telegram.telegram_service import authorize_user, create_stars_invoice
from app.services.crypto.cryptopay import create_crypto_invoice
from app.services.payment.platega import platega_service
from platega.types import PaymentMethod

from app.utils.helper import calculate_rub_to_crypto, calculate_rub_to_stars, response, convert_to_decimal

router = APIRouter()


@router.post(
    "/stars",
    response_model=ResponseSchema[TransactionOut]
)
async def deposit_stars(
    deposit_in: DepositIn,
    repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo)
) -> ResponseSchema[TransactionOut]:
    """
    Create a deposit with stars.
    """

    user_data = await authorize_user(deposit_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    stars_amount = await calculate_rub_to_stars(
        amount_rub=deposit_in.amount
    )

    transaction = await repo.create(
        user_id=user.user_id,
        amount=stars_amount,
        rub_amount=convert_to_decimal(deposit_in.amount),
        service="telegram",
        currency="STARS"
    )

    invoice_link = await create_stars_invoice(
        amount=stars_amount,
        payload=str(transaction.id)
    )

    await repo.update_payment_link(
        transaction_id=transaction.id,
        payment_link=invoice_link
    )

    return response(
        data=transaction,
        model=TransactionOut,
        message="Transaction created successfully"
    )



@router.post(
    "/cryptopay",
    response_model=ResponseSchema[TransactionOut]
)
async def deposit_cryptopay(
    deposit_in: DepositIn,
    repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo)
):
    """Create cryptopay deposit"""
    user_data = await authorize_user(deposit_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    transaction = await repo.create(
        user_id=user.user_id,
        amount=deposit_in.amount,
        rub_amount=convert_to_decimal(deposit_in.amount),
        service="cryptopay",
        currency="USD"
    )

    usd_amount = await calculate_rub_to_crypto(
        amount_rub=convert_to_decimal(deposit_in.amount)
    )

    invoice_link, invoice_id = await create_crypto_invoice(
        amount=float(usd_amount),
        payload=str(transaction.id)
    )

    await repo.update_payment_link(
        transaction_id=transaction.id,
        payment_link=invoice_link
    )

    await repo.update_transaction_hash(
        transaction_id=transaction.id,
        transaction_hash=str(invoice_id)
    )

    return response(
        data=transaction,
        model=TransactionOut,
        message="Transaction created successfully"
    )


@router.post(
    "/platega",
    response_model=ResponseSchema[TransactionOut]
)
async def deposit_platega(
    deposit_in: DepositIn,
    repo: TransactionRepository = Depends(get_transaction_repo),
    user_repo: UserRepository = Depends(get_user_repo)
):
    """Create Platega deposit"""
    user_data = await authorize_user(deposit_in.init_data)

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    transaction = await repo.create(
        user_id=user.user_id,
        amount=deposit_in.amount,
        rub_amount=convert_to_decimal(deposit_in.amount),
        service="platega",
        currency="RUB"
    )

    result = await platega_service.create_transaction(
        amount=deposit_in.amount,
        currency="RUB",
        description=f"Deposit #{transaction.id}",
        return_url=f"https://t.me/smmly_bot/app?startapp=success",
        failed_url=f"https://t.me/smmly_bot/app?startapp=failed",
        payload=str(transaction.id),
    )

    await repo.update_payment_link(
        transaction_id=transaction.id,
        payment_link=result.payment_link or ""
    )

    await repo.update_transaction_hash(
        transaction_id=transaction.id,
        transaction_hash=str(result.transaction_id)
    )

    return response(
        data=transaction,
        model=TransactionOut,
        message="Transaction created successfully"
    )