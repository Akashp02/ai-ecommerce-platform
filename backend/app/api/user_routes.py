from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.user_service import register_user
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return register_user(
        db=db,
        user=user
    )

@router.get("/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user
