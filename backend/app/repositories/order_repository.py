from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(
    db: Session,
    db_order: Order
):

    db.add(db_order)
    db.flush()

    return db_order


def create_order_item(
    db: Session,
    db_order_item: OrderItem
):

    db.add(db_order_item)


def get_user_orders(
    db: Session,
    user_id: int
):

    return (
        db.query(Order)
        .filter(
            Order.user_id == user_id
        )
        .all()
    )


def get_order_by_id(
    db: Session,
    order_id: int
):

    return (
        db.query(Order)
        .filter(
            Order.id == order_id
        )
        .first()
    )