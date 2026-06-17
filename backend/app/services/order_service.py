from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem

from app.schemas.order import OrderCreate

from app.repositories.order_repository import create_order
from app.repositories.order_repository import create_order_item
from app.repositories.order_repository import get_user_orders
from app.repositories.order_repository import get_order_by_id
from app.repositories.order_repository import get_order_items
from app.repositories.order_repository import update_order

from app.repositories.address_repository import get_address_by_id
from app.repositories.product_repository import get_product_by_id

from app.core.logger import logger


def place_order(
    db: Session,
    order_data: OrderCreate,
    current_user
):

    logger.info(
        f"Order creation started | User ID={current_user.id}"
    )

    address = get_address_by_id(
        db=db,
        address_id=order_data.address_id
    )

    if not address:

        logger.error(
            f"Order failed | Address not found | Address ID={order_data.address_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    if address.user_id != current_user.id:

        logger.error(
            f"Unauthorized address usage | User ID={current_user.id} | Address ID={order_data.address_id}"
        )

        raise HTTPException(
            status_code=403,
            detail="Invalid address"
        )

    total_amount = 0
    order_items_data = []

    for item in order_data.items:

        product = get_product_by_id(
            db=db,
            product_id=item.product_id
        )

        if not product:

            logger.error(
                f"Order failed | Product not found | Product ID={item.product_id}"
            )

            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock_quantity < item.quantity:

            logger.error(
                f"Insufficient stock | Product ID={product.id} | Available={product.stock_quantity} | Requested={item.quantity}"
            )

            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        subtotal = product.price * item.quantity

        total_amount += subtotal

        order_items_data.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price,
            "subtotal": subtotal
        })

    try:

        db_order = Order(
            user_id=current_user.id,
            address_id=order_data.address_id,
            total_amount=total_amount
        )

        db_order = create_order(
            db=db,
            db_order=db_order
        )

        for item in order_items_data:

            db_order_item = OrderItem(
                order_id=db_order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price_at_purchase=item["price"],
                subtotal=item["subtotal"]
            )

            create_order_item(
                db=db,
                db_order_item=db_order_item
            )

            item["product"].stock_quantity -= item["quantity"]

            logger.info(
                f"Stock deducted | Product ID={item['product'].id} | Quantity={item['quantity']}"
            )

            if item["product"].stock_quantity == 0:
                item["product"].is_available = False

        db.commit()
        db.refresh(db_order)

        logger.info(
            f"Order created successfully | Order ID={db_order.id} | User ID={current_user.id} | Amount={total_amount}"
        )

        return db_order

    except Exception as e:

        db.rollback()

        logger.error(
            f"Order transaction failed | User ID={current_user.id} | Error={str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Order creation failed"
        )


def list_orders(
    db: Session,
    current_user
):

    logger.info(
        f"Fetching orders | User ID={current_user.id}"
    )

    return get_user_orders(
        db=db,
        user_id=current_user.id
    )


def fetch_order(
    db: Session,
    order_id: int,
    current_user
):

    logger.info(
        f"Fetching order details | Order ID={order_id} | User ID={current_user.id}"
    )

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if not order:

        logger.error(
            f"Order not found | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.user_id != current_user.id:

        logger.error(
            f"Unauthorized order access | Order ID={order_id} | User ID={current_user.id}"
        )

        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    items = get_order_items(
        db=db,
        order_id=order_id
    )

    return {
        "id": order.id,
        "total_amount": order.total_amount,
        "order_status": order.order_status,
        "payment_status": order.payment_status,
        "items": items
    }


def update_order_status(
    db: Session,
    order_id: int,
    order_status
):

    logger.info(
        f"Order status update initiated | Order ID={order_id}"
    )

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if not order:

        logger.error(
            f"Order status update failed | Order not found | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if (
        order.order_status == "shipped"
        and order_status == "cancelled"
    ):

        logger.error(
            f"Invalid cancellation attempt | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="Cannot cancel shipped order"
        )

    order.order_status = order_status

    logger.info(
        f"Order status updated | Order ID={order_id} | New Status={order_status}"
    )

    return update_order(
        db=db,
        db_order=order
    )


def update_payment_status(
    db: Session,
    order_id: int,
    payment_status
):

    logger.info(
        f"Payment status update initiated | Order ID={order_id}"
    )

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if not order:

        logger.error(
            f"Payment status update failed | Order not found | Order ID={order_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.payment_status = payment_status

    logger.info(
        f"Payment status updated | Order ID={order_id} | New Status={payment_status}"
    )

    return update_order(
        db=db,
        db_order=order
    )