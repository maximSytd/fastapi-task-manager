from fastapi import APIRouter

from api.example.example import example_router
from api.users.user import user_router
from api.tasks.task import task_router

router = APIRouter()
router.include_router(example_router, prefix="/api/examples")
router.include_router(user_router, prefix="/api/users")
router.include_router(task_router, prefix="/api/tasks")

__all__ = ["router"]
