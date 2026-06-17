from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_user

from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewUpdate
from app.schemas.review import ReviewResponse

from app.services.review_service import add_review
from app.services.review_service import modify_review
from app.services.review_service import list_product_reviews
from app.services.review_service import remove_review


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post(
    "/products/{product_id}",
    response_model=ReviewResponse
)
def create_review(
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return add_review(
        db=db,
        product_id=product_id,
        review=review,
        current_user=current_user
    )


@router.put(
    "/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return modify_review(
        db=db,
        review_id=review_id,
        review_data=review,
        current_user=current_user
    )


@router.get(
    "/products/{product_id}",
    response_model=list[ReviewResponse]
)
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):

    return list_product_reviews(
        db=db,
        product_id=product_id
    )


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return remove_review(
        db=db,
        review_id=review_id,
        current_user=current_user
    )