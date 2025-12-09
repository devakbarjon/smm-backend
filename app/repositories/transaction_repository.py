from decimal import Decimal

from .base import BaseRepository

from app.models.transaction import Transaction

from app.enums.status import TransactionStatusEnum


class TransactionRepository(BaseRepository):

    async def create(
        self,
        amount: Decimal,
        rub_amount: Decimal,
        service: str,
        user_id: int,
        status: TransactionStatusEnum = TransactionStatusEnum.pending,
        currency: str = "RUB",
        transaction_hash: str | None = None,
        payment_link: str | None = None
    ) -> Transaction:
        transaction = Transaction(
            amount=amount,
            rub_amount=rub_amount,
            service=service,
            user_id=user_id,
            status=status,
            currency=currency,
            transaction_hash=transaction_hash,
            payment_link=payment_link
        )
        return await self.add(transaction)

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        return await self.get_one(Transaction, id=transaction_id)

    async def get_by_user_id(self, user_id: int) -> list[Transaction]:
        return await self.get_many(Transaction, user_id=user_id)

    async def update_status(self, transaction_id: int, status: TransactionStatusEnum) -> Transaction | None:
        transaction = await self.get_by_id(transaction_id)
        if transaction:
            transaction.status = status
            await self.update(transaction)
        return transaction
