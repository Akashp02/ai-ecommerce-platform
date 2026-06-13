from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(
    db: Session,
    product: ProductCreate,
    is_available: bool,
):

    db_product = Product(
        sku=product.sku,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        is_available=is_available,
    )

    db.add(db_product)

    db.commit()

    db.refresh(db_product)

    return db_product


def get_all_products(
    db: Session,
):

    return (
        db.query(Product)
        .all()
    )


def get_product_by_id(
    db: Session,
    product_id: int,
):

    return (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )


def get_product_by_sku(
    db: Session,
    sku: str,
):

    return (
        db.query(Product)
        .filter(
            Product.sku == sku
        )
        .first()
    )

def update_product(
    db: Session,
    db_product: Product,
):

    db.commit()

    db.refresh(db_product)

    return db_product