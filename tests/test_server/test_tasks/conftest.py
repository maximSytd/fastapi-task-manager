import pytest_asyncio

from app.db.models import User, Task
from app.db.factories import AsyncTaskFactory


@pytest_asyncio.fixture(scope="module")
async def multiple_tasks_for_test_user(test_user: User) -> list[Task]:
    """Return 3 Task instance related to test_user for tests."""
    return await AsyncTaskFactory.create_batch(size=3, user=test_user)


@pytest_asyncio.fixture(scope="module")
async def task_for_test_user(multiple_tasks_for_test_user: list[Task]) -> Task:
    """Return first Task instance from multiple tasks fixture."""
    return multiple_tasks_for_test_user[0]


@pytest_asyncio.fixture(scope="module")
async def builded_task_for_test_user(test_user: User) -> Task:
    """Return builded Task instance related to test_user for tests."""
    return await AsyncTaskFactory.build(user=test_user)