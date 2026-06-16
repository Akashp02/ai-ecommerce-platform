from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.address import Address
from app.schemas.address import AddressCreate
from app.schemas.address import AddressUpdate

from app.repositories.address_repository import create_address
from app.repositories.address_repository import get_user_addresses
from app.repositories.address_repository import get_default_address
from app.repositories.address_repository import get_address_by_id
from app.repositories.address_repository import update_address
from app.repositories.address_repository import delete_address


def add_address(
    db: Session,
    address: AddressCreate,
    current_user,
):

    if address.is_default:

        old_default = get_default_address(
            db=db,
            user_id=current_user.id
        )

        if old_default:
            old_default.is_default = False


    db_address = Address(
        user_id=current_user.id,
        full_name=address.full_name.strip(),
        phone_number=address.phone_number.strip(),
        address_line1=address.address_line1.strip(),
        address_line2=address.address_line2,
        city=address.city.strip().title(),
        state=address.state.strip().title(),
        country=address.country.strip().title(),
        postal_code=address.postal_code.strip(),
        is_default=address.is_default
    )

    return create_address(
        db=db,
        db_address=db_address
    )


def list_addresses(
    db: Session,
    current_user,
):

    return get_user_addresses(
        db=db,
        user_id=current_user.id
    )


def modify_address(
    db: Session,
    address_id: int,
    address_data: AddressUpdate,
    current_user,
):

    db_address = get_address_by_id(
        db=db,
        address_id=address_id
    )

    if not db_address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    if db_address.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    if address_data.is_default:

        old_default = get_default_address(
            db=db,
            user_id=current_user.id
        )

        if old_default and old_default.id != address_id:
            old_default.is_default = False


    db_address.full_name = address_data.full_name
    db_address.phone_number = address_data.phone_number
    db_address.address_line1 = address_data.address_line1
    db_address.address_line2 = address_data.address_line2
    db_address.city = address_data.city
    db_address.state = address_data.state
    db_address.country = address_data.country
    db_address.postal_code = address_data.postal_code
    db_address.is_default = address_data.is_default

    return update_address(
        db=db,
        db_address=db_address
    )


def remove_address(
    db: Session,
    address_id: int,
    current_user,
):

    db_address = get_address_by_id(
        db=db,
        address_id=address_id
    )

    if not db_address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    if db_address.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    if db_address.is_default:
        raise HTTPException(
            status_code=400,
            detail="Default address cannot be deleted"
        )

    delete_address(
        db=db,
        db_address=db_address
    )

    return {
        "message": "Address deleted successfully"
    }