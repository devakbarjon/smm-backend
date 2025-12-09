from fastapi import APIRouter, Depends, HTTPException

from app.schemas.base import ResponseSchema
from app.schemas.deposit import DepositIn
from app.schemas.transaction import TransactionOut

from app.dependencies.repositories import get_transaction_repo, get_user_repo

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository

from app.services.telegram.telegram_service import authorize_user, create_stars_invoice

from app.utils.helper import response, convert_to_decimal

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
        raise HTTPException(status_code=404, detail="User not found!")

    transaction = await repo.create(
        user_id=user.user_id,
        amount=convert_to_decimal(deposit_in.amount),
        rub_amount=convert_to_decimal(deposit_in.amount),
        service="telegram",
        currency="STARS"
    )

    invoice_link = await create_stars_invoice(
        amount=deposit_in.amount,
        payload=str(transaction.id)
    )

    transaction.payment_link = invoice_link
    await repo.update(transaction)

    return response(
        data=transaction,
        model=TransactionOut,
        message="Transaction created successfully"
    )