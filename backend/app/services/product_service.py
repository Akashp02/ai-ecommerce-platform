from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate

from app.repositories.product_repository import create_product
from app.repositories.product_repository import get_all_products
from app.repositories.product_repository import get_product_by_id
from app.repositories.product_repository import get_product_by_sku
from app.repositories.product_repository import update_product

from app.repositories.category_repository import get_category_by_id


def calculate_availability(
    stock_quantity: int,
):

    return stock_quantity > 0


def add_product(
    db: Session,
    product: ProductCreate,
):

    # Step 1: Normalize input

    normalized_sku = product.sku.strip().upper()
    normalized_name = product.name.strip().title()


    # Step 2: Validate category exists

    category = get_category_by_id(
        db=db,
        category_id=product.category_id,
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )


    # Step 3: Check duplicate SKU

    existing_product = get_product_by_sku(
        db=db,
        sku=normalized_sku,
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )


    # Step 4: Determine availability

    is_available = calculate_availability(
        product.stock_quantity
    )


    # Step 5: Create product

    return create_product(
        db=db,
        category_id=product.category_id,
        sku=normalized_sku,
        name=normalized_name,
        price=product.price,
        stock_quantity=product.stock_quantity,
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


    # Step 2: Update allowed fields
    # SKU should NEVER change

    db_product.name = (
        product_data.name
        .strip()
        .title()
    )

    db_product.price = product_data.price

    db_product.stock_quantity = (
        product_data.stock_quantity
    )


    # Step 3: Recalculate availability

    db_product.is_available = (
        calculate_availability(
            product_data.stock_quantity
        )
    )


    # Step 4: Save changes

    return update_product(
        db=db,
        db_product=db_product,
    )