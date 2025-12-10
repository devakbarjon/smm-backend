from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from starlette import status

from soc_proof.models import OrderStatus

from app.schemas.base import ResponseSchema
from app.schemas.order import OrderIn, OrderOut, OrderStatusOut, OrderStatusListOut, OrderStatusIn
from app.schemas.user import UserIn

from app.repositories.order_repository import OrderRepository
from app.dependencies.repositories import get_order_repo
from app.repositories.user_repository import UserRepository
from app.dependencies.repositories import get_user_repo
from app.repositories.service_repository import ServiceRepository
from app.dependencies.repositories import get_service_repo

from app.services.smm.smm_service import smm_service
from app.services.telegram.telegram_service import authorize_user

from app.utils.helper import response, list_response, calculate_cost

router = APIRouter()


@router.post("/", response_model=ResponseSchema[OrderOut])
async def create_order(
    order_in: OrderIn,
    order_repo: OrderRepository = Depends(get_order_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    service_repo: ServiceRepository = Depends(get_service_repo),
) -> ResponseSchema[OrderOut]:
    """
    Create a new order.
    """

    user_data = await authorize_user(order_in.init_data)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid init_data signature!")

    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    service = await service_repo.get_by_id(order_in.service_id)

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found!")

    cost = calculate_cost(price=service.price, quantity=order_in.quantity)

    if user.balance < cost:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance!")

    user.balance -= cost
    await user_repo.update(user)

    parent_order_id = await smm_service.create_order(
        service_id=order_in.service_id,
        link=order_in.link,
        quantity=order_in.quantity
    )

    order = await order_repo.create(
        user_id=user.user_id,
        service_id=order_in.service_id,
        parent_order_id=int(parent_order_id),
        link=order_in.link,
        quantity=order_in.quantity,
        cost=cost
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid init_data signature!")
    
    user = await user_repo.get_by_id(user_data.user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    order = await order_repo.get_by_user_and_order_id(
        user_id=user.user_id,
        order_id=status_in.order_id
    )

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")

    parent_order_list = await smm_service.get_order_status(orders=str(order.parent_order_id))
    parent_order: OrderStatus = parent_order_list[0] if parent_order_list else None

    order_out = OrderStatusOut(
        id=order.id,
        quantity=order.quantity,
        link=order.link,
        cost=order.cost,
        service_id=order.service_id,
        charge=parent_order.charge,
        status=parent_order.status.lower(),
        remains=parent_order.remains
    )

    return response(
        data=order_out,
        model=OrderStatusOut,
        message="Order status fetched successfully"
    )


@router.post("/list", response_model=ResponseSchema[OrderStatusListOut])
async def list_orders(
    user_in: UserIn,
    order_repo: OrderRepository = Depends(get_order_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> ResponseSchema[OrderStatusListOut]:
    """
    List all orders for a user.
    """
    user_data = await authorize_user(user_in.init_data)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid init_data signature!")

    user = await user_repo.get_by_id(user_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    orders = await order_repo.get_by_user_id(user_id=user.user_id)

    orders_out_list = []
    if orders:
        parent_order_ids = [order.parent_order_id for order in orders if order.parent_order_id]

        if parent_order_ids:
            parent_orders_statuses = await smm_service.get_order_status(orders=parent_order_ids)
            status_map = {str(status.order_id): status for status in parent_orders_statuses}

            for order in orders:
                parent_order_status = status_map.get(str(order.parent_order_id))
                if parent_order_status:
                    orders_out_list.append(OrderStatusOut(
                        id=order.id,
                        quantity=order.quantity,
                        link=order.link,
                        cost=order.cost,
                        service_id=order.service_id,
                        charge=parent_order_status.charge,
                        status=parent_order_status.status.lower(),
                        remains=parent_order_status.remains
                    ))

    return list_response(
        data={"orders": orders_out_list},
        model=OrderStatusListOut,
        message="Orders fetched successfully"
    )
