from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user_repository import create_user
from app.repositories.user_repository import get_user_by_email
from app.schemas.user import UserCreate
from app.core.security import verify_password

def register_user(
    db: Session,
    user: UserCreate,
):

    existing_user = get_user_by_email(
        db=db,
        email=user.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    user.password = hash_password(
        user.password
    )
    return create_user(
        db=db,
        user=user,
    )

def authenticate_user(
    db: Session,
    email: str,
    password: str,
):

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return user