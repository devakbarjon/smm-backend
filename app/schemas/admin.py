from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.enums.language import LangEnum
from app.enums.status import TransactionStatusEnum


# Users
class UserBase(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    lang: Optional[LangEnum] = LangEnum.ru
    balance: Optional[Decimal] = Field(default=Decimal("0.00"), decimal_places=2)
    ref_id: Optional[int] = None
    ref_income: Optional[Decimal] = Field(default=Decimal("0.00"), decimal_places=2)


class UserCreate(UserBase):
    user_id: int
    ref_code: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    lang: Optional[LangEnum] = None
    balance: Optional[Decimal] = None
    ref_id: Optional[int] = None
    ref_income: Optional[Decimal] = None


class UserResponse(UserBase):
    user_id: int
    ref_code: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Orders
class OrderBase(BaseModel):
    service_id: int
    quantity: int
    link: str = Field(..., max_length=500)
    cost: Optional[Decimal] = Field(None, decimal_places=2)
    is_done: bool = False
    parent_order_id: Optional[int] = None


class OrderCreate(OrderBase):
    user_id: Optional[int] = None


class OrderUpdate(BaseModel):
    service_id: Optional[int] = None
    quantity: Optional[int] = None
    link: Optional[str] = None
    cost: Optional[Decimal] = None
    is_done: Optional[bool] = None
    parent_order_id: Optional[int] = None
    user_id: Optional[int] = None


class OrderResponse(OrderBase):
    id: int
    user_id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Services
class ServiceBase(BaseModel):
    name: str = Field(..., max_length=255)
    api_service_id: int
    price: Decimal = Field(..., decimal_places=2)
    original_price: Decimal = Field(..., decimal_places=2)
    description: Optional[str] = None
    language: LangEnum
    time: Optional[str] = Field(None, max_length=100)
    refill: bool = False
    cancel: bool = False
    min_amount: int
    max_amount: int
    type: str = Field(..., max_length=50)


class ServiceCreate(ServiceBase):
    category_id: int


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    api_service_id: Optional[int] = None
    price: Optional[Decimal] = None
    original_price: Optional[Decimal] = None
    description: Optional[str] = None
    language: Optional[LangEnum] = None
    time: Optional[str] = None
    refill: Optional[bool] = None
    cancel: Optional[bool] = None
    min_amount: Optional[int] = None
    max_amount: Optional[int] = None
    type: Optional[str] = None
    category_id: Optional[int] = None


class ServiceResponse(ServiceBase):
    id: int
    category_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Categories
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)


class CategoryCreate(CategoryBase):
    platform_id: int


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    platform_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    platform_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Platforms
class PlatformBase(BaseModel):
    name: str = Field(..., max_length=100)
    keywords: str = ""


class PlatformCreate(PlatformBase):
    pass


class PlatformUpdate(BaseModel):
    name: Optional[str] = None
    keywords: Optional[str] = None


class PlatformResponse(PlatformBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Transactions
class TransactionBase(BaseModel):
    transaction_hash: Optional[str] = None
    currency: str = Field(default="RUB", max_length=10)
    amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    rub_amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    service: str = Field(..., max_length=100)
    payment_link: Optional[str] = None
    status: TransactionStatusEnum = TransactionStatusEnum.pending


class TransactionCreate(TransactionBase):
    user_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    transaction_hash: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[Decimal] = None
    rub_amount: Optional[Decimal] = None
    service: Optional[str] = None
    payment_link: Optional[str] = None
    status: Optional[TransactionStatusEnum] = None
    user_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Settings
class SettingBase(BaseModel):
    markup_rate: Decimal = Field(..., decimal_places=2)
    ton_rate: Decimal = Field(..., decimal_places=2)
    min_deposit_rate: Decimal = Field(default=Decimal("0.00"), decimal_places=2)


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    markup_rate: Optional[Decimal] = None
    ton_rate: Optional[Decimal] = None
    min_deposit_rate: Optional[Decimal] = None


class SettingResponse(SettingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



class AdminKeyVerify(BaseModel):
    key: str


class AdminKeyVerifyResponse(BaseModel):
    valid: bool
