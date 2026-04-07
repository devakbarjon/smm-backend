from decimal import Decimal
from sqlalchemy import select, func

from .base import BaseRepository

from app.models.transaction import Transaction

from app.enums.status import TransactionStatusEnum


class TransactionRepository(BaseRepository):

    async def create(
        self,
        amount: Decimal | float,
        rub_amount: Decimal | float,
        service: str,
        user_id: int,
        status: TransactionStatusEnum = TransactionStatusEnum.pending,
        currency: str = "RUB",
        transaction_hash: str | None = None,
        payment_link: str | None = None
    ) -> Transaction:
        
        amount = Decimal(amount)
        rub_amount = Decimal(rub_amount)
        
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
        return await self.get_all(Transaction, user_id=user_id, status=TransactionStatusEnum.success)

    async def get_total_transactions(self) -> int:
        return await self.get_count(Transaction)

    async def get_total_completed_revenue(self) -> Decimal:
        stmt = (
            select(func.coalesce(func.sum(Transaction.rub_amount), 0))
            .where(Transaction.status == TransactionStatusEnum.success)
        )
        result = await self.session.execute(stmt)
        value = result.scalar()
        return Decimal(str(value or 0))

    async def update_status(self, transaction_id: int, status: TransactionStatusEnum) -> Transaction | None:
        transaction = await self.get_by_id(transaction_id)
        if transaction:
            transaction.status = status
            await self.update(transaction)
        return transaction
    
    async def update_payment_link(self, transaction_id: int, payment_link: str) -> Transaction | None:
        transaction = await self.get_by_id(transaction_id)
        if transaction:
            transaction.payment_link = payment_link
            await self.update(transaction)
        return transaction
    
    async def update_transaction_hash(self, transaction_id: int, transaction_hash: str | int) -> Transaction | None:
        transaction = await self.get_by_id(transaction_id)
        if transaction:
            transaction.transaction_hash = str(transaction_hash)
            await self.update(transaction)
        return transaction