from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    UserResponse,
    TokenResponse
)

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_username = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    hashed_password = hash_password(
        data.password
    )


    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
        role=data.role,
        is_active=True
    )


    db.add(user)

    db.commit()

    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )


    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user