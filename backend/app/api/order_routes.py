from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_user

from app.schemas.order import OrderCreate
from app.schemas.order import OrderResponse

from app.services.order_service import place_order
from app.services.order_service import list_orders
from app.services.order_service import fetch_order


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
    response_model=OrderResponse
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