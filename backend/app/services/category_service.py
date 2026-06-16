from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.category import CategoryCreate
from app.repositories.category_repository import create_category
from app.repositories.category_repository import get_category_by_name
from app.repositories.category_repository import get_all_categories


def generate_slug(
    name: str,
):

    return (
        name
        .strip()
        .lower()
        .replace(" ", "-")
    )


def add_category(
    db: Session,
    category: CategoryCreate,
):

    # Normalize input

    category_name = category.name.strip()


    # Duplicate check

    existing_category = get_category_by_name(
        db=db,
        name=category_name,
    )

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )


    # Generate slug

    slug = generate_slug(
        category_name
    )


    # Format name for storage

    formatted_name = category_name.title()


    return create_category(
        db=db,
        name=formatted_name,
        description=category.description,
        slug=slug,
    )


def list_categories(
    db: Session,
):

    return get_all_categories(
        db=db
    )