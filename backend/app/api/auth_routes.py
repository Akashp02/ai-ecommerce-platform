from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_db
from app.services.user_service import authenticate_user
from app.core.security import create_access_token
from app.schemas.auth import TokenResponse
from app.schemas.user import ChangePasswordRequest
from app.services.user_service import change_password
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.put(
    "/change-password"
)
def update_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return change_password(
        db=db,
        password_data=password_data,
        current_user=current_user
    )