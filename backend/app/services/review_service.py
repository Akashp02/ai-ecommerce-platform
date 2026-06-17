from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product_review import ProductReview

from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewUpdate

from app.repositories.review_repository import get_review_by_user_product
from app.repositories.review_repository import check_user_purchased_product
from app.repositories.review_repository import create_review
from app.repositories.review_repository import update_review
from app.repositories.review_repository import get_product_reviews
from app.repositories.review_repository import get_review_by_id
from app.repositories.review_repository import delete_review

from app.repositories.product_repository import get_product_by_id


def add_review(
    db: Session,
    product_id: int,
    review: ReviewCreate,
    current_user
):

    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    purchased = check_user_purchased_product(
        db=db,
        user_id=current_user.id,
        product_id=product_id
    )

    if not purchased:
        raise HTTPException(
            status_code=400,
            detail="Purchase product before reviewing"
        )


    existing_review = get_review_by_user_product(
        db=db,
        user_id=current_user.id,
        product_id=product_id
    )

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="Review already exists"
        )


    db_review = ProductReview(
        product_id=product_id,
        user_id=current_user.id,
        rating=review.rating,
        review_text=review.review_text.strip()
    )

    return create_review(
        db=db,
        db_review=db_review
    )


def modify_review(
    db: Session,
    review_id: int,
    review_data: ReviewUpdate,
    current_user
):

    review = get_review_by_id(
        db=db,
        review_id=review_id
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    review.rating = review_data.rating
    review.review_text = review_data.review_text

    return update_review(
        db=db,
        db_review=review
    )


def list_product_reviews(
    db: Session,
    product_id: int
):

    return get_product_reviews(
        db=db,
        product_id=product_id
    )


def remove_review(
    db: Session,
    review_id: int,
    current_user
):

    review = get_review_by_id(
        db=db,
        review_id=review_id
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    delete_review(
        db=db,
        db_review=review
    )

    return {
        "message": "Review deleted successfully"
    }