from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem

from app.schemas.order import OrderCreate

from app.repositories.order_repository import create_order
from app.repositories.order_repository import create_order_item
from app.repositories.order_repository import get_user_orders
from app.repositories.order_repository import get_order_by_id

from app.repositories.address_repository import get_address_by_id
from app.repositories.product_repository import get_product_by_id


def place_order(
    db: Session,
    order_data: OrderCreate,
    current_user,
):

    address = get_address_by_id(
        db=db,
        address_id=order_data.address_id
    )

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    if address.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Invalid address"
        )


    total_amount = 0
    order_items_data = []


    # Validate products

    for item in order_data.items:

        product = get_product_by_id(
            db=db,
            product_id=item.product_id
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock_quantity < item.quantity:
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

        # Create order

        db_order = Order(
            user_id=current_user.id,
            address_id=order_data.address_id,
            total_amount=total_amount
        )

        db_order = create_order(
            db=db,
            db_order=db_order
        )


        # Create order items + deduct stock

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


            # Deduct stock

            item["product"].stock_quantity -= item["quantity"]


            # Recalculate availability

            if item["product"].stock_quantity == 0:
                item["product"].is_available = False


        db.commit()
        db.refresh(db_order)

        return db_order


    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Order creation failed"
        )


def list_orders(
    db: Session,
    current_user
):

    return get_user_orders(
        db=db,
        user_id=current_user.id
    )


def fetch_order(
    db: Session,
    order_id: int,
    current_user
):

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    return order