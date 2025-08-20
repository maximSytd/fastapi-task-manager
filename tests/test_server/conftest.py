import pytest_asyncio
from httpx import AsyncClient

from app.db.models import User
from app.db.factories import AsyncUserFactory
from app.services.auth import create_access_token


@pytest_asyncio.fixture(scope="module")
async def test_user() -> User:
    """Return user instance for tests."""
    return await AsyncUserFactory.create()


@pytest_asyncio.fixture(scope="module")
async def test_user_token(test_user: User) -> str:
    """Return test user auth token."""
    return create_access_token(data={"sub": test_user.username})


@pytest_asyncio.fixture(scope="module")
async def invalid_test_user_token(test_user: User) -> str:
    """Return invalid auth token."""
    return create_access_token(data={"sub": test_user.username[::-1]})


@pytest_asyncio.fixture(scope="module")
async def authorized_async_client(
    async_client: AsyncClient,
    test_user_token: str,
) -> AsyncClient:
    """Return and provide auth token to async client."""
    async_client.headers.update(
        {
            "Authorization": f"Bearer {test_user_token}",
        },
    )
    return async_client
