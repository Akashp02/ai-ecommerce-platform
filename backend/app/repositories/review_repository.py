from sqlalchemy.orm import Session

from app.models.product_review import ProductReview
from app.models.order import Order
from app.models.order_item import OrderItem


def get_review_by_user_product(
    db: Session,
    user_id: int,
    product_id: int
):

    return (
        db.query(ProductReview)
        .filter(
            ProductReview.user_id == user_id,
            ProductReview.product_id == product_id
        )
        .first()
    )


def check_user_purchased_product(
    db: Session,
    user_id: int,
    product_id: int
):

    order = (
        db.query(OrderItem)
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.user_id == user_id,
            OrderItem.product_id == product_id
        )
        .first()
    )

    return order


def create_review(
    db: Session,
    db_review: ProductReview
):

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def update_review(
    db: Session,
    db_review: ProductReview
):

    db.commit()
    db.refresh(db_review)

    return db_review


def get_product_reviews(
    db: Session,
    product_id: int
):

    return (
        db.query(ProductReview)
        .filter(
            ProductReview.product_id == product_id
        )
        .all()
    )


def get_review_by_id(
    db: Session,
    review_id: int
):

    return (
        db.query(ProductReview)
        .filter(
            ProductReview.id == review_id
        )
        .first()
    )


def delete_review(
    db: Session,
    db_review: ProductReview
):

    db.delete(db_review)
    db.commit()