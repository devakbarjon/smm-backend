from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.base import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.service_repository import ServiceRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.platform_repository import PlatformRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.setting_repository import SettingRepository

from app.models.user import User
from app.models.order import Order
from app.models.service import Service
from app.models.category import Category
from app.models.platform import Platform
from app.models.transaction import Transaction
from app.models.setting import Setting

from app.schemas.admin import (
    UserCreate, UserUpdate, UserResponse,
    OrderCreate, OrderUpdate, OrderResponse,
    ServiceCreate, ServiceUpdate, ServiceResponse,
    CategoryCreate, CategoryUpdate, CategoryResponse,
    PlatformCreate, PlatformUpdate, PlatformResponse,
    TransactionCreate, TransactionUpdate, TransactionResponse,
    SettingCreate, SettingUpdate, SettingResponse,
    AdminKeyVerify, AdminKeyVerifyResponse
)
from app.schemas.base import ResponseSchema
from app.core.config import settings

router = APIRouter()


@router.post("/verify-key", response_model=AdminKeyVerifyResponse)
async def verify_admin_key(data: AdminKeyVerify):
    """Verify if the provided admin key is valid"""
    is_valid = data.key == settings.ADMIN_KEY.get_secret_value()
    return AdminKeyVerifyResponse(valid=is_valid)


@router.get("/users", response_model=ResponseSchema[List[UserResponse]])
async def get_all_users(
    session: AsyncSession = Depends(get_db)
):
    """Get all users"""
    repo = UserRepository(session)
    users = await repo.get_all(User)
    return ResponseSchema(data=users)


@router.get("/users/{user_id}", response_model=ResponseSchema[UserResponse])
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific user by ID"""
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return ResponseSchema(data=user)


@router.post("/users", response_model=ResponseSchema[UserResponse])
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    repo = UserRepository(session)
    
    existing_user = await repo.get_by_id(user_data.user_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this ID already exists"
        )
    
    user = User(**user_data.model_dump())
    created_user = await repo.add(user)
    return ResponseSchema(data=created_user)


@router.put("/users/{user_id}", response_model=ResponseSchema[UserResponse])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a user"""
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    updated_user = await repo.update(user, **update_data)
    return ResponseSchema(data=updated_user)


@router.delete("/users/{user_id}", response_model=ResponseSchema[dict])
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a user"""
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await repo.delete(user)
    return ResponseSchema(data={"deleted": True})


@router.get("/orders", response_model=ResponseSchema[List[OrderResponse]])
async def get_all_orders(
    session: AsyncSession = Depends(get_db)
):
    """Get all orders"""
    repo = OrderRepository(session)
    orders = await repo.get_all(Order)
    return ResponseSchema(data=orders)


@router.get("/orders/{order_id}", response_model=ResponseSchema[OrderResponse])
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific order by ID"""
    repo = OrderRepository(session)
    order = await repo.get_one(Order, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return ResponseSchema(data=order)


@router.post("/orders", response_model=ResponseSchema[OrderResponse])
async def create_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new order"""
    repo = OrderRepository(session)
    order = Order(**order_data.model_dump())
    created_order = await repo.add(order)
    return ResponseSchema(data=created_order)


@router.put("/orders/{order_id}", response_model=ResponseSchema[OrderResponse])
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update an order"""
    repo = OrderRepository(session)
    order = await repo.get_one(Order, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    update_data = order_data.model_dump(exclude_unset=True)
    updated_order = await repo.update(order, **update_data)
    return ResponseSchema(data=updated_order)


@router.delete("/orders/{order_id}", response_model=ResponseSchema[dict])
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete an order"""
    repo = OrderRepository(session)
    order = await repo.get_one(Order, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    await repo.delete(order)
    return ResponseSchema(data={"deleted": True})


@router.get("/services", response_model=ResponseSchema[List[ServiceResponse]])
async def get_all_services(
    session: AsyncSession = Depends(get_db)
):
    """Get all services"""
    repo = ServiceRepository(session)
    services = await repo.get_all(Service)
    return ResponseSchema(data=services)


@router.get("/services/{service_id}", response_model=ResponseSchema[ServiceResponse])
async def get_service(
    service_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific service by ID"""
    repo = ServiceRepository(session)
    service = await repo.get_one(Service, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return ResponseSchema(data=service)


@router.post("/services", response_model=ResponseSchema[ServiceResponse])
async def create_service(
    service_data: ServiceCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new service"""
    repo = ServiceRepository(session)
    service = Service(**service_data.model_dump())
    created_service = await repo.add(service)
    return ResponseSchema(data=created_service)


@router.put("/services/{service_id}", response_model=ResponseSchema[ServiceResponse])
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a service"""
    repo = ServiceRepository(session)
    service = await repo.get_one(Service, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    update_data = service_data.model_dump(exclude_unset=True)
    updated_service = await repo.update(service, **update_data)
    return ResponseSchema(data=updated_service)


@router.delete("/services/{service_id}", response_model=ResponseSchema[dict])
async def delete_service(
    service_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a service"""
    repo = ServiceRepository(session)
    service = await repo.get_one(Service, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    await repo.delete(service)
    return ResponseSchema(data={"deleted": True})


@router.get("/categories", response_model=ResponseSchema[List[CategoryResponse]])
async def get_all_categories(
    session: AsyncSession = Depends(get_db)
):
    """Get all categories"""
    repo = CategoryRepository(session)
    categories = await repo.get_all(Category)
    return ResponseSchema(data=categories)


@router.get("/categories/{category_id}", response_model=ResponseSchema[CategoryResponse])
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific category by ID"""
    repo = CategoryRepository(session)
    category = await repo.get_one(Category, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return ResponseSchema(data=category)


@router.post("/categories", response_model=ResponseSchema[CategoryResponse])
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new category"""
    repo = CategoryRepository(session)
    category = Category(**category_data.model_dump())
    created_category = await repo.add(category)
    return ResponseSchema(data=created_category)


@router.put("/categories/{category_id}", response_model=ResponseSchema[CategoryResponse])
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a category"""
    repo = CategoryRepository(session)
    category = await repo.get_one(Category, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = category_data.model_dump(exclude_unset=True)
    updated_category = await repo.update(category, **update_data)
    return ResponseSchema(data=updated_category)


@router.delete("/categories/{category_id}", response_model=ResponseSchema[dict])
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a category"""
    repo = CategoryRepository(session)
    category = await repo.get_one(Category, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    await repo.delete(category)
    return ResponseSchema(data={"deleted": True})


@router.get("/platforms", response_model=ResponseSchema[List[PlatformResponse]])
async def get_all_platforms(
    session: AsyncSession = Depends(get_db)
):
    """Get all platforms"""
    repo = PlatformRepository(session)
    platforms = await repo.get_all(Platform)
    return ResponseSchema(data=platforms)


@router.get("/platforms/{platform_id}", response_model=ResponseSchema[PlatformResponse])
async def get_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific platform by ID"""
    repo = PlatformRepository(session)
    platform = await repo.get_one(Platform, id=platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    return ResponseSchema(data=platform)


@router.post("/platforms", response_model=ResponseSchema[PlatformResponse])
async def create_platform(
    platform_data: PlatformCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new platform"""
    repo = PlatformRepository(session)
    platform = Platform(**platform_data.model_dump())
    created_platform = await repo.add(platform)
    return ResponseSchema(data=created_platform)


@router.put("/platforms/{platform_id}", response_model=ResponseSchema[PlatformResponse])
async def update_platform(
    platform_id: int,
    platform_data: PlatformUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a platform"""
    repo = PlatformRepository(session)
    platform = await repo.get_one(Platform, id=platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    
    update_data = platform_data.model_dump(exclude_unset=True)
    updated_platform = await repo.update(platform, **update_data)
    return ResponseSchema(data=updated_platform)


@router.delete("/platforms/{platform_id}", response_model=ResponseSchema[dict])
async def delete_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a platform"""
    repo = PlatformRepository(session)
    platform = await repo.get_one(Platform, id=platform_id)
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    
    await repo.delete(platform)
    return ResponseSchema(data={"deleted": True})


@router.get("/transactions", response_model=ResponseSchema[List[TransactionResponse]])
async def get_all_transactions(
    session: AsyncSession = Depends(get_db)
):
    """Get all transactions"""
    repo = TransactionRepository(session)
    transactions = await repo.get_all(Transaction)
    return ResponseSchema(data=transactions)


@router.get("/transactions/{transaction_id}", response_model=ResponseSchema[TransactionResponse])
async def get_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific transaction by ID"""
    repo = TransactionRepository(session)
    transaction = await repo.get_one(Transaction, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return ResponseSchema(data=transaction)


@router.post("/transactions", response_model=ResponseSchema[TransactionResponse])
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new transaction"""
    repo = TransactionRepository(session)
    transaction = Transaction(**transaction_data.model_dump())
    created_transaction = await repo.add(transaction)
    return ResponseSchema(data=created_transaction)


@router.put("/transactions/{transaction_id}", response_model=ResponseSchema[TransactionResponse])
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a transaction"""
    repo = TransactionRepository(session)
    transaction = await repo.get_one(Transaction, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    update_data = transaction_data.model_dump(exclude_unset=True)
    updated_transaction = await repo.update(transaction, **update_data)
    return ResponseSchema(data=updated_transaction)


@router.delete("/transactions/{transaction_id}", response_model=ResponseSchema[dict])
async def delete_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a transaction"""
    repo = TransactionRepository(session)
    transaction = await repo.get_one(Transaction, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    await repo.delete(transaction)
    return ResponseSchema(data={"deleted": True})


@router.get("/settings", response_model=ResponseSchema[List[SettingResponse]])
async def get_all_settings(
    session: AsyncSession = Depends(get_db)
):
    """Get all settings"""
    repo = SettingRepository(session)
    settings_list = await repo.get_all(Setting)
    return ResponseSchema(data=settings_list)


@router.get("/settings/{setting_id}", response_model=ResponseSchema[SettingResponse])
async def get_setting(
    setting_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get a specific setting by ID"""
    repo = SettingRepository(session)
    setting = await repo.get_one(Setting, id=setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    return ResponseSchema(data=setting)


@router.post("/settings", response_model=ResponseSchema[SettingResponse])
async def create_setting(
    setting_data: SettingCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create a new setting"""
    repo = SettingRepository(session)
    setting = Setting(**setting_data.model_dump())
    created_setting = await repo.add(setting)
    return ResponseSchema(data=created_setting)


@router.put("/settings/{setting_id}", response_model=ResponseSchema[SettingResponse])
async def update_setting(
    setting_id: int,
    setting_data: SettingUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Update a setting"""
    repo = SettingRepository(session)
    setting = await repo.get_one(Setting, id=setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    update_data = setting_data.model_dump(exclude_unset=True)
    updated_setting = await repo.update(setting, **update_data)
    return ResponseSchema(data=updated_setting)


@router.delete("/settings/{setting_id}", response_model=ResponseSchema[dict])
async def delete_setting(
    setting_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Delete a setting"""
    repo = SettingRepository(session)
    setting = await repo.get_one(Setting, id=setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    await repo.delete(setting)
    return ResponseSchema(data={"deleted": True})
