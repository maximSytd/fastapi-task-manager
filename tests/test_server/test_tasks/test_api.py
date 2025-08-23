import datetime

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)

from app.db.models import Task
from tests.utils import is_valid_uuid
from app.api.tasks.rest import TASK_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_task_api_list(
    authorized_async_client: AsyncClient,
    multiple_tasks_for_test_user: list[Task],
):
    """Ensure that user can get list of tasks."""
    response = await authorized_async_client.get(
        "api/tasks",
        params={
            "page": 1,
            "size": 50,
        },
        follow_redirects=True,
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert len(response_body["items"]) == len(multiple_tasks_for_test_user)


@pytest.mark.asyncio
async def test_task_api_create(
    authorized_async_client: AsyncClient,
    builded_task_for_test_user: Task,
):
    """Ensure that authenticated user can create task."""
    response = await authorized_async_client.post(
        "api/tasks",
        json={
            "title": builded_task_for_test_user.title,
            "description": builded_task_for_test_user.description,
        },
        follow_redirects=True,
    )
    response_body = response.json()
    assert response.status_code == HTTP_201_CREATED, response_body
    assert is_valid_uuid(response_body["id"])
    assert response_body["title"] == builded_task_for_test_user.title
    assert response_body["description"] == (
        builded_task_for_test_user.description
    )
    assert response_body["status"]["value"] == Task.StatusChoices.CREATED.value
    assert response_body["status"]["label"]
    assert response_body["created"]
    assert response_body["modified"]


@pytest.mark.asyncio
async def test_task_api_get(
    authorized_async_client: AsyncClient,
    task_for_test_user: Task,
):
    """Ensure that authenticated user can get task by id."""
    response = await authorized_async_client.get(
        f"api/tasks/{task_for_test_user.id}",
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["id"] == str(task_for_test_user.id)
    assert response_body["title"] == task_for_test_user.title
    assert response_body["description"] == task_for_test_user.description
    assert response_body["status"]["value"] == task_for_test_user.status.value
    assert response_body["status"]["label"]
    assert datetime.datetime.fromisoformat(
        response_body["created"].replace(
            "Z",
            "+00:00",
            ),
        ) == task_for_test_user.created
    assert datetime.datetime.fromisoformat(
        response_body["modified"].replace(
            "Z",
            "+00:00",
            ),
        ) == task_for_test_user.modified


@pytest.mark.asyncio
async def test_task_api_update(
    authorized_async_client: AsyncClient,
    task_for_test_user: Task,
    builded_task_for_test_user: Task,
):
    """Ensure that authenticated user can update task by id."""
    response = await authorized_async_client.put(
        f"api/tasks/{task_for_test_user.id}",
        json={
            "title": builded_task_for_test_user.title,
            "description": builded_task_for_test_user.description,
            "status": builded_task_for_test_user.status,
        },
    )
    response_body = response.json()
    assert response.status_code == HTTP_200_OK, response_body
    assert response_body["id"] == str(task_for_test_user.id)
    assert response_body["title"] == builded_task_for_test_user.title
    assert response_body["description"] == (
        builded_task_for_test_user.description
    )
    assert response_body["status"]["value"] == (
        builded_task_for_test_user.status.value
    )
    assert response_body["status"]["label"]


@pytest.mark.asyncio
async def test_task_api_delete(
    authorized_async_client: AsyncClient,
    task_for_test_user: Task,
):
    """Ensure that authenticated user can delete task by id."""
    response = await authorized_async_client.delete(
        f"api/tasks/{task_for_test_user.id}",
        follow_redirects=True,
    )
    assert response.status_code == HTTP_204_NO_CONTENT
    assert await Task.get_or_none(id=task_for_test_user.id) is None

@pytest.mark.parametrize(
    "http_method, use_data",
    [
        [
            "get",
            False,
        ],
        [
            "put",
            True,
        ],
        [
            "delete",
            False,
        ],
    ],
)
@pytest.mark.asyncio
async def test_invalid_id_task_api(
    authorized_async_client: AsyncClient,
    builded_task_for_test_user: Task,
    http_method: str,
    use_data: bool,
):
    """Ensure that authenticated user can touch only existing tasks by id."""
    object_url = f"api/tasks/{builded_task_for_test_user.id}"
    async_api_request = authorized_async_client.__getattribute__(http_method)
    if not use_data:
        response = await async_api_request(url=object_url)
    else:
        response = await async_api_request(
        url=object_url,
        json={
            "title": builded_task_for_test_user.title,
        }
    )
    assert response.status_code == HTTP_404_NOT_FOUND, response.text

@pytest.mark.asyncio
async def test_access_control_task_api_get(
    unfair_authorized_async_client: AsyncClient,
    task_for_test_user: Task,
):
    """Ensure that api have restrict access for get other user tasks."""
    response = await unfair_authorized_async_client.get(
        f"api/tasks/{task_for_test_user.id}",
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == TASK_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_access_control_task_api_update(
    unfair_authorized_async_client: AsyncClient,
    task_for_test_user: Task,
):
    """Ensure that api have restrict access for update other user tasks."""
    response = await unfair_authorized_async_client.put(
        f"api/tasks/{task_for_test_user.id}",
        json={
            "title": task_for_test_user.title,
        }
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == TASK_NOT_FOUND_MESSAGE


@pytest.mark.asyncio
async def test_access_control_task_api_delete(
    unfair_authorized_async_client: AsyncClient,
    task_for_test_user: Task,
):
    """Ensure that api have restrict access for delete other user tasks."""
    response = await unfair_authorized_async_client.delete(
        f"api/tasks/{task_for_test_user.id}",
    )
    response_body = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response_body["detail"] == TASK_NOT_FOUND_MESSAGE
