import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment

from app.repositories.payment_repository import create_payment
from app.repositories.order_repository import get_order_by_id
from app.repositories.order_repository import update_order

from app.core.logger import logger


def process_payment(
    db: Session,
    order_id: int,
    payment_method,
    current_user
):

    # Step 1: Payment initiation log

    logger.info(
        f"Payment initiated | Order ID={order_id} | User ID={current_user.id}"
    )


    # Step 2: Check order exists

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if not order:

        logger.error(
            f"Payment failed | Order not found | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    # Step 3: Check ownership

    if order.user_id != current_user.id:

        logger.error(
            f"Unauthorized payment attempt | Order ID={order_id} | User ID={current_user.id}"
        )

        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )


    # Step 4: Check duplicate payment

    if order.payment_status == "paid":

        logger.error(
            f"Duplicate payment attempt | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="Already paid"
        )


    # Step 5: Fake payment simulation

    payment_success = True

    transaction_id = str(
        uuid.uuid4()
    )


    # Step 6: Process payment result

    if payment_success:

        payment_status = "paid"

        order.payment_status = "paid"
        order.order_status = "confirmed"

        logger.info(
            f"Payment successful | Order ID={order_id} | Transaction ID={transaction_id}"
        )

    else:

        payment_status = "failed"

        order.payment_status = "failed"

        logger.error(
            f"Payment failed | Order ID={order_id}"
        )


    # Step 7: Create payment record

    db_payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        payment_method=payment_method,
        payment_status=payment_status,
        transaction_id=transaction_id
    )


    payment = create_payment(
        db=db,
        db_payment=db_payment
    )


    # Step 8: Update order status

    update_order(
        db=db,
        db_order=order
    )

    logger.info(
        f"Order updated after payment | Order ID={order_id} | Payment Status={payment_status}"
    )


    # Step 9: Return payment

    return payment