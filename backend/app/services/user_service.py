from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.security import verify_password

from app.repositories.user_repository import create_user
from app.repositories.user_repository import get_user_by_email

from app.schemas.user import UserCreate

from app.core.logger import logger


def register_user(
    db: Session,
    user: UserCreate,
):

    # Step 1: Log registration attempt

    logger.info(
        f"User registration attempt | Email={user.email}"
    )


    # Step 2: Check duplicate email

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


    # Step 3: Hash password

    user.password = hash_password(
        user.password
    )


    # Step 4: Create user

    db_user = create_user(
        db=db,
        user=user,
    )


    # Step 5: Success log

    logger.info(
        f"User registered successfully | User ID={db_user.id} | Email={db_user.email}"
    )

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):

    # Step 1: Login attempt

    logger.info(
        f"Login attempt | Email={email}"
    )


    # Step 2: Check user exists

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


    # Step 3: Verify password

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


    # Step 4: Login success

    logger.info(
        f"Login successful | User ID={user.id} | Email={email}"
    )

    return user