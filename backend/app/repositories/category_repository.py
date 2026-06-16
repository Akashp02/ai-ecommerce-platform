from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.category import Category


def create_category(
    db: Session,
    name: str,
    description: str,
    slug: str,
):

    db_category = Category(
        name=name,
        slug=slug,
        description=description,
    )

    db.add(db_category)

    db.commit()

    db.refresh(db_category)

    return db_category


def get_category_by_name(
    db: Session,
    name: str,
):

    return (
        db.query(Category)
        .filter(
            func.lower(Category.name) == name.lower()
        )
        .first()
    )


def get_all_categories(
    db: Session,
):

    return (
        db.query(Category)
        .filter(
            Category.is_active == True
        )
        .all()
    )

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