import enum


class TransactionStatusEnum(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"