from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.api.deps import get_current_admin

from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryResponse

from app.services.category_service import add_category
from app.services.category_service import list_categories


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "",
    response_model=CategoryResponse
)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin),
):

    return add_category(
        db=db,
        category=category,
    )


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db),
):

    return list_categories(
        db=db
    )