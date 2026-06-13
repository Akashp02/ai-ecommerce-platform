from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate

from app.repositories.product_repository import create_product
from app.repositories.product_repository import get_all_products
from app.repositories.product_repository import get_product_by_id
from app.repositories.product_repository import get_product_by_sku
from app.schemas.product import ProductUpdate
from app.repositories.product_repository import update_product

def add_product(
    db: Session,
    product: ProductCreate,
):

    # Check duplicate SKU (Business Validation)

    existing_product = get_product_by_sku(
        db=db,
        sku=product.sku,
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    # Business Logic for availability

    is_available = True

    if product.stock_quantity == 0:
        is_available = False

    return create_product(
        db=db,
        product=product,
        is_available=is_available,
    )


def list_products(
    db: Session,
):

    return get_all_products(
        db=db
    )


def fetch_product(
    db: Session,
    product_id: int,
):

    product = get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

def update_existing_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
):

    # Step 1: Check if product exists

    db_product = get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    # Step 2: Check duplicate SKU

    existing_product = get_product_by_sku(
        db=db,
        sku=product_data.sku,
    )

    if (
        existing_product
        and existing_product.id != product_id
    ):
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )


    # Step 3: Update fields

    db_product.sku = product_data.sku
    db_product.name = product_data.name
    db_product.description = product_data.description
    db_product.price = product_data.price
    db_product.stock_quantity = product_data.stock_quantity


    # Step 4: Recalculate availability

    if product_data.stock_quantity == 0:
        db_product.is_available = False
    else:
        db_product.is_available = True


    # Step 5: Save changes

    return update_product(
        db=db,
        db_product=db_product,
    )