from pydantic import BaseModel, ConfigDict
from datetime import datetime

from decimal import Decimal

from app.enums.status import TransactionStatusEnum


class TransactionStarsIn(BaseModel):
    secret_key: str = "app-secret-key"  # secret_key of app that sent telegram bot
    amount: int  # amount in telegram stars
    transaction_id: int  # Id of transaction in database
    transaction_hash: str  # Transaction hash from telegram
    user_id: int


class TransactionOut(BaseModel):
    id: int
    amount: Decimal
    rub_amount: Decimal
    transaction_hash: str | None = None
    service: str
    status: TransactionStatusEnum
    currency: str
    payment_link: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)