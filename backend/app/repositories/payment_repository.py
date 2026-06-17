from sqlalchemy.orm import Session

from app.models.payment import Payment


def create_payment(
    db: Session,
    db_payment: Payment
):

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_payment_by_order_id(
    db: Session,
    order_id: int
):

    return (
        db.query(Payment)
        .filter(
            Payment.order_id == order_id
        )
        .first()
    )