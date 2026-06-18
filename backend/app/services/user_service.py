from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.security import verify_password

from app.repositories.user_repository import create_user
from app.repositories.user_repository import get_user_by_email
from app.repositories.user_repository import update_user_password

from app.schemas.user import UserCreate
from app.schemas.user import ChangePasswordRequest

from app.core.logger import logger


def register_user(
    db: Session,
    user: UserCreate,
):

    logger.info(
        f"User registration attempt | Email={user.email}"
    )

    existing_user = get_user_by_email(
        db=db,
        email=user.email,
    )

    if existing_user:

        logger.error(
            f"Duplicate email registration attempt | Email={user.email}"
        )

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user.password = hash_password(
        user.password
    )

    db_user = create_user(
        db=db,
        user=user,
    )

    logger.info(
        f"User registered successfully | User ID={db_user.id} | Email={db_user.email}"
    )

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):

    logger.info(
        f"Login attempt | Email={email}"
    )

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if not user:

        logger.error(
            f"Login failed | User not found | Email={email}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash,
    ):

        logger.error(
            f"Login failed | Wrong password | Email={email}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    logger.info(
        f"Login successful | User ID={user.id} | Email={email}"
    )

    return user


def change_password(
    db: Session,
    password_data: ChangePasswordRequest,
    current_user,
):

    logger.info(
        f"Password change attempt | User ID={current_user.id}"
    )

    # Step 1 Verify old password

    if not verify_password(
        password_data.old_password,
        current_user.password_hash
    ):

        logger.error(
            f"Password change failed | Wrong old password | User ID={current_user.id}"
        )

        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )


    # Step 2 Prevent same password

    if verify_password(
        password_data.new_password,
        current_user.password_hash
    ):

        logger.error(
            f"Password change failed | Same password used | User ID={current_user.id}"
        )

        raise HTTPException(
            status_code=400,
            detail="New password cannot be same as old password"
        )


    # Step 3 Hash new password

    current_user.password_hash = hash_password(
        password_data.new_password
    )


    # Step 4 Update DB

    update_user_password(
        db=db,
        user=current_user
    )


    logger.info(
        f"Password changed successfully | User ID={current_user.id}"
    )

    return {
        "message": "Password updated successfully"
    }