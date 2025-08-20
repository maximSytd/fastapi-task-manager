from fastapi import APIRouter

from api.users.user import user_router
from api.tasks.task import task_router

router = APIRouter()
router.include_router(
    user_router,
    prefix="/api/users",
    tags=[
        "User",
    ],
)
router.include_router(
    task_router,
    prefix="/api/tasks",
    tags=[
        "Tasks",
    ],
)

__all__ = [
    "router",
]
