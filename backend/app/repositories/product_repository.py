from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.category import Category

def create_product(
    db: Session,
    category_id: int,
    sku: str,
    name: str,
    price: float,
    stock_quantity: int,
    is_available: bool,
):

    db_product = Product(
        category_id=category_id,
        sku=sku,
        name=name,
        price=price,
        stock_quantity=stock_quantity,
        is_available=is_available,
    )

    db.add(db_product)

    db.commit()

    db.refresh(db_product)

    return db_product


def get_product_by_sku(
    db: Session,
    sku: str,
):

    return (
        db.query(Product)
        .filter(
            func.lower(Product.sku) == sku.lower()
        )
        .first()
    )


def get_product_by_id(
    db: Session,
    product_id: int,
):

    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.is_active == True
        )
        .first()
    )


def get_all_products(
    db: Session,
):

    return (
        db.query(Product)
        .filter(
            Product.is_active == True
        )
        .all()
    )


def update_product(
    db: Session,
    db_product: Product,
):

    db.commit()

    db.refresh(db_product)

    return db_product

def get_category_by_id(
    db: Session,
    category_id: int,
):

    return (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.is_active == True
        )
        .first()
    )