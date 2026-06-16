from sqlalchemy.orm import Session

from app.models.address import Address


def create_address(
    db: Session,
    db_address: Address,
):

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


def get_user_addresses(
    db: Session,
    user_id: int,
):

    return (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .all()
    )


def get_default_address(
    db: Session,
    user_id: int,
):

    return (
        db.query(Address)
        .filter(
            Address.user_id == user_id,
            Address.is_default == True
        )
        .first()
    )


def get_address_by_id(
    db: Session,
    address_id: int,
):

    return (
        db.query(Address)
        .filter(Address.id == address_id)
        .first()
    )


def update_address(
    db: Session,
    db_address: Address,
):

    db.commit()
    db.refresh(db_address)

    return db_address


def delete_address(
    db: Session,
    db_address: Address,
):

    db.delete(db_address)
    db.commit()