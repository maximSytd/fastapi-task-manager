from fastapi_babel import _
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)

from db.models import User
from services.auth import decode_access_token

UNAUTHORIZED_DETAIL_MESSAGE = "Invalid authentication credentials"
USER_NOT_FOUND_DETAIL_MESSAGE = "User not found"
NOT_ADMIN_DETAIL_MESSAGE = "Administrator rights required"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Return and decode user from jwt token."""
    username = decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=_(UNAUTHORIZED_DETAIL_MESSAGE),
        )
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(USER_NOT_FOUND_DETAIL_MESSAGE),
        )
    return user

def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """Return and check if user is admin."""
    if not user.is_admin:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=_(NOT_ADMIN_DETAIL_MESSAGE),
        )
    return user
