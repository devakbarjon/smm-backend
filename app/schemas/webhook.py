from pydantic import BaseModel


class WebhookIn(BaseModel):
    transaction_id: int
    transaction_hash: str
    amount: int
    secret_key: str