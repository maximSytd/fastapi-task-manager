import uuid

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

ClientManagerType = AsyncGenerator[AsyncClient, None]


@asynccontextmanager
async def client_manager(
    app,
    base_url="http://test",
    **kw,
) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url=base_url,
            **kw,
        ) as c:
            yield c


def is_valid_uuid(uuid_to_test, version=4):
    """Return bool and check if uuid_to_test is a valid UUID."""
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
