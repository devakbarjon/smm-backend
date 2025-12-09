from fastapi import APIRouter, Depends, HTTPException

from app.schemas.base import ResponseSchema
from app.schemas.order import OrderIn, OrderOut, OrderStatusOut, OrderStatusListOut, OrderStatusIn

from app.repositories.order_repository import OrderRepository
from app.dependencies.repositories import get_order_repo
from app.repositories.user_repository import UserRepository
from app.dependencies.repositories import get_user_repo

from app.services.smm.smm_service import smm_service
from app.services.telegram.telegram_service import authorize_user

from app.utils.helper import response, list_response


router = APIRouter()


@router.post("/", response_model=ResponseSchema[OrderOut])
async def create_order(
    order_in: OrderIn,
    order_repo: OrderRepository = Depends(get_order_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> ResponseSchema[OrderOut]:
    """
    Create a new order.
    """

    user_data = await authorize_user(order_in.init_data)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid init_data signature!")

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    parent_order_id = await smm_service.create_order(
        service_id=order_in.service_id,
        link=order_in.link,
        quantity=order_in.quantity
    )

    order = await order_repo.create(
        user_id=user.user_id,
        service_id=order_in.service_id,
        oder_id=parent_order_id,
        link=order_in.link,
        quantity=order_in.quantity
    )

    return response(
        data=order,
        model=OrderOut,
        message="Order created successfully"
    )


@router.post("/status", response_model=ResponseSchema[OrderStatusOut])
async def get_order_status(
    status_in: OrderStatusIn,
    order_repo: OrderRepository = Depends(get_order_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> ResponseSchema[OrderStatusOut]:
    """
    Get the status of an order.
    """

    user_data = await authorize_user(status_in.init_data)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid init_data signature!")
    
    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    order = await order_repo.get_by_user_and_order_id(
        user_id=user.user_id,
        order_id=status_in.order_id
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found!")

    return response(
        data=order,
        model=OrderStatusOut,
        message="Order status fetched successfully"
    )


@router.post("/list", response_model=ResponseSchema[OrderStatusListOut])
async def list_orders(
    status_in: OrderStatusIn,
    order_repo: OrderRepository = Depends(get_order_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> ResponseSchema[OrderStatusListOut]:
    """
    List all orders for a user.
    """

    user_data = await authorize_user(status_in.init_data)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid init_data signature!")
    
    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    orders = await order_repo.get_by_user_id(user_id=user.user_id)

    return list_response(
        data=orders,
        model=OrderStatusListOut,
        message="Orders fetched successfully"
    )