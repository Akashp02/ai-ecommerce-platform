from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_user

from app.schemas.address import AddressCreate
from app.schemas.address import AddressUpdate
from app.schemas.address import AddressResponse

from app.services.address_service import add_address
from app.services.address_service import list_addresses
from app.services.address_service import modify_address
from app.services.address_service import remove_address


router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"]
)


@router.post(
    "",
    response_model=AddressResponse
)
def create_new_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return add_address(
        db=db,
        address=address,
        current_user=current_user
    )


@router.get(
    "",
    response_model=list[AddressResponse]
)
def get_addresses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return list_addresses(
        db=db,
        current_user=current_user
    )


@router.put(
    "/{address_id}",
    response_model=AddressResponse
)
def update_existing_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return modify_address(
        db=db,
        address_id=address_id,
        address_data=address,
        current_user=current_user
    )


@router.delete("/{address_id}")
def delete_existing_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    return remove_address(
        db=db,
        address_id=address_id,
        current_user=current_user
    )