from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_user
from app.api.deps import get_current_admin

from app.schemas.order import OrderCreate
from app.schemas.order import OrderResponse
from app.schemas.order import OrderDetailResponse
from app.schemas.order import OrderStatusUpdate
from app.schemas.order import PaymentStatusUpdate

from app.services.order_service import place_order
from app.services.order_service import list_orders
from app.services.order_service import fetch_order
from app.services.order_service import update_order_status
from app.services.order_service import update_payment_status


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "",
    response_model=OrderResponse
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return place_order(
        db=db,
        order_data=order,
        current_user=current_user
    )


@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return list_orders(
        db=db,
        current_user=current_user
    )


@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return fetch_order(
        db=db,
        order_id=order_id,
        current_user=current_user
    )


@router.put(
    "/{order_id}/status",
    response_model=OrderResponse
)
def change_order_status(
    order_id: int,
    status: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):

    return update_order_status(
        db=db,
        order_id=order_id,
        order_status=status.order_status
    )


@router.put(
    "/{order_id}/payment",
    response_model=OrderResponse
)
def change_payment_status(
    order_id: int,
    status: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):

    return update_payment_status(
        db=db,
        order_id=order_id,
        payment_status=status.payment_status
    )