from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_user

from app.schemas.payment import PaymentCreate
from app.schemas.payment import PaymentResponse

from app.services.payment_service import process_payment


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/{order_id}",
    response_model=PaymentResponse
)
def make_payment(
    order_id: int,
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return process_payment(
        db=db,
        order_id=order_id,
        payment_method=payment.payment_method,
        current_user=current_user
    )