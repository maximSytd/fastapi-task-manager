import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from app.db.models import User
from app.db.factories.user import DEFAULT_PASSWORD
from app.services.auth import decode_access_token
from app.api.users.messages import (
    INCORRECT_CREDENTIALS_MESSAGE,
    USERNAME_ALREADY_EXIST_MESSAGE,
)

USERS_API_PATH = "/api/v1/users"

@pytest.mark.asyncio
async def test_user_api_register(async_client: AsyncClient):
    """Ensure that user can register."""
    test_username = "nagibator1337"
    response = await async_client.post(
        USERS_API_PATH + "/register",
        json={
            "username": test_username,
            "password": "super_secret_password",
        }
    )
    response_body = response.json()
    assert response.status_code == HTTP_201_CREATED, response_body
    assert response_body["username"] == test_username
    assert isinstance(response_body["id"], int)


@pytest.mark.asyncio
async def test_invalid_user_api_register(
    async_client: AsyncClient,
    test_user: User,
):
    """Ensure that user can't register with existing username."""
    response = await async_client.post(
        USERS_API_PATH + "/register",
        json={
            "username": test_user.username,
            "password": "super_secret_password",
        }
    )
    response_body = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST, response_body
    assert response.json()["detail"] == USERNAME_ALREADY_EXIST_MESSAGE


@pytest.mark.asyncio
async def test_user_api_login(async_client: AsyncClient, test_user: User):
    """Ensure that user can login with credentials."""
    response = await async_client.post(
        USERS_API_PATH + "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": test_user.username,
            "password": DEFAULT_PASSWORD,
        }
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["token_type"] == "bearer"
    assert decode_access_token(
        response_body["access_token"],
    ) == test_user.username


@pytest.mark.asyncio
async def test_invalid_user_api_login_wrong_password(
    async_client: AsyncClient,
    test_user: User,
):
    """Ensure that user can't login with wrong password."""
    response = await async_client.post(
        USERS_API_PATH + "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": test_user.username,
            "password": "incorrect_password",
        }
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INCORRECT_CREDENTIALS_MESSAGE


@pytest.mark.asyncio
async def test_invalid_user_api_login_nonexistent_user(
    async_client: AsyncClient,
):
    """Ensure that user can't login with non-existent username."""
    response = await async_client.post(
        USERS_API_PATH + "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "password",
            "username": "non_existent_username",
            "password": DEFAULT_PASSWORD,
        }
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INCORRECT_CREDENTIALS_MESSAGE
