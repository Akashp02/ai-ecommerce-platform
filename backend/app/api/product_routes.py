from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.schemas.product import ProductCreate
from app.schemas.product import ProductResponse

from app.services.product_service import add_product
from app.services.product_service import list_products
from app.services.product_service import fetch_product
from app.api.deps import get_current_admin
from app.schemas.product import ProductUpdate
from app.services.product_service import update_existing_product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create Product (For now no admin auth)
@router.post(
    "",
    response_model=ProductResponse
)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):

    return add_product(
        db=db,
        product=product,
    )


# Public endpoint
@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db),
):

    return list_products(
        db=db
    )


# Public endpoint
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_single_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    return fetch_product(
        db=db,
        product_id=product_id,
    )

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_existing_product_route(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):

    return update_existing_product(
        db=db,
        product_id=product_id,
        product_data=product,
    )