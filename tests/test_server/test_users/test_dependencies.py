import pytest
from httpx import AsyncClient
from fastapi import HTTPException

from app.db.models import User
from app.dependencies.auth import (
    get_current_user,
    UNAUTHORIZED_DETAIL_MESSAGE,
    USER_NOT_FOUND_DETAIL_MESSAGE,
)
from app.services.auth import create_access_token


@pytest.mark.asyncio
async def test_get_current_user(
    async_client: AsyncClient,
    test_user: User,
    test_user_token: str,
):
    """Ensure that dependency return correct username."""
    assert test_user == await get_current_user(token=test_user_token)


@pytest.mark.asyncio
async def test_no_username_get_current_user(
    async_client: AsyncClient,
    invalid_test_user_token: str,
):
    """Ensure that dependency raise error with incorrect username."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=invalid_test_user_token)
    assert USER_NOT_FOUND_DETAIL_MESSAGE in str(exc_info.value)


@pytest.mark.asyncio
async def test_user_not_found_get_current_user(async_client: AsyncClient):
    """Ensure that dependency raise error with incorrect jwt."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=create_access_token({"alg": "HS256"}))
    assert UNAUTHORIZED_DETAIL_MESSAGE in str(exc_info.value)
