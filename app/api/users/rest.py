from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist, IntegrityError
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from db.models import User
from db import schemas
from services.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
)
from .messages import (
    INCORRECT_CREDENTIALS_MESSAGE,
    USERNAME_ALREADY_EXIST_MESSAGE,
)

user_router_rest = APIRouter()

@user_router_rest.post(
    "/token",
    response_model=schemas.Token,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": INCORRECT_CREDENTIALS_MESSAGE,
        }
    }
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user with OAuth form."""
    try:
        user = await User.get(username=form_data.username)
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=INCORRECT_CREDENTIALS_MESSAGE,
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=INCORRECT_CREDENTIALS_MESSAGE,
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router_rest.post(
    "/register",
    response_model=schemas.UserOut,
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_400_BAD_REQUEST: {
            "description": USERNAME_ALREADY_EXIST_MESSAGE,
        },
    }
)
async def register(user: schemas.UserCreate):
    """Register new user."""
    hashed_password = get_password_hash(user.password)
    try:
        new_user = await User.create(
            username=user.username,
            password_hash=hashed_password
        )
        return new_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=USERNAME_ALREADY_EXIST_MESSAGE,
        )
