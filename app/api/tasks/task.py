import uuid

from fastapi_babel import _
from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import paginate
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)

from db import schemas
from db.models import User, Task
from dependencies.auth import get_current_user

task_router = APIRouter()

TASK_NOT_FOUND_MESSAGE = "Task not found"

@task_router.get("/", response_model=Page[schemas.TaskOut])
async def list_tasks(current_user: User = Depends(get_current_user)):
    """List all tasks for user."""
    return await paginate(Task.filter(user=current_user))


@task_router.get(
    "/{task_id}",
    response_model=schemas.TaskOut,
)
async def get_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
):
    """Get a specific task (for user)."""
    try:
        return await Task.get(
            id=task_id,
            user=current_user,
        )
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(TASK_NOT_FOUND_MESSAGE),
        )


@task_router.post(
    "/",
    response_model=schemas.TaskOut,
    status_code=HTTP_201_CREATED,
)
async def create_task(
    task_data: schemas.TaskCreate,
    current_user: User = Depends(get_current_user),
):
    """Create new task (for user)."""
    return await Task.create(
        title=task_data.title,
        description=task_data.description,
        user=current_user,
    )


@task_router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(
    task_id: uuid.UUID,
    task_data: schemas.TaskUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update existing task (for user)."""
    try:
        task = await Task.get(
            id=task_id,
            user=current_user,
        )
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(TASK_NOT_FOUND_MESSAGE),
        )

    if task_data.title:
        task.title = task_data.title
    if task_data.description:
        task.description = task_data.description
    if task_data.status:
        task.status = task_data.status

    await task.save()
    return task


@task_router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
):
    """Delete a task (for user)."""
    deleted_count = await Task.filter(id=task_id, user=current_user).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=_(TASK_NOT_FOUND_MESSAGE),
        )
