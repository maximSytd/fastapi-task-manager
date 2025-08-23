from fastapi import APIRouter

from api.users.rest import user_router_rest
from api.users.graphql import user_router_graphql
from api.tasks.rest import task_router_rest
from api.tasks.graphql import task_router_graphql

router = APIRouter()
router.include_router(
    user_router_rest,
    prefix="/api/v1/users",
    tags=[
        "User",
    ],
)
router.include_router(
    user_router_graphql,
    prefix="/api/v1/users/graphql",
    tags=[
        "User",
    ],
)
router.include_router(
    task_router_rest,
    prefix="/api/v1/tasks",
    tags=[
        "Tasks",
    ],
)
router.include_router(
    task_router_graphql,
    prefix="/api/v1/tasks/graphql",
    tags=[
        "Tasks",
    ],
)

__all__ = [
    "router",
]
