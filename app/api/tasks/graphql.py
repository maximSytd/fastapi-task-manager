import uuid
import strawberry
from typing import List
from strawberry.types import Info
from strawberry.fastapi import GraphQLRouter
from tortoise.exceptions import DoesNotExist
from strawberry.exceptions import StrawberryGraphQLError

from db.models import Task, User
from db.graphql import TaskType, TaskCreateInput, TaskUpdateInput
from ..permissions import IsAuthenticated
from ..context import get_graphql_context
from .messages import TASK_NOT_FOUND_MESSAGE


@strawberry.type
class TaskQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def tasks(self, info: Info) -> List[TaskType]:
        """List all tasks for the current user"""
        user: User = info.context["user"]
        return await Task.filter(user=user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def task(self, info: Info, task_id: uuid.UUID) -> TaskType:
        """Get a specific task for the current user"""
        user: User = info.context["user"]
        try:
            return await Task.get(id=task_id, user=user)
        except DoesNotExist:
            raise StrawberryGraphQLError(message=TASK_NOT_FOUND_MESSAGE)


@strawberry.type
class TaskMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_task(self, info: Info, task_data: TaskCreateInput) -> TaskType:
        """Create new task for user"""
        user: User = info.context["user"]
        task = await Task.create(
            title=task_data.title,
            description=task_data.description,
            user=user,
        )
        return task

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_task(
        self, info: Info, task_id: uuid.UUID, task_data: TaskUpdateInput
    ) -> TaskType:
        """Update existing task for user"""
        user: User = info.context["user"]
        try:
            task = await Task.get(id=task_id, user=user)
        except DoesNotExist:
            raise StrawberryGraphQLError(message=TASK_NOT_FOUND_MESSAGE)

        if task_data.title:
            task.title = task_data.title
        if task_data.description:
            task.description = task_data.description
        if task_data.status:
            task.status = task_data.status

        await task.save()
        return task

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_task(self, info: Info, task_id: uuid.UUID) -> bool:
        """Delete task for user"""
        user: User = info.context["user"]
        deleted_count = await Task.filter(id=task_id, user=user).delete()
        if not deleted_count:
            raise StrawberryGraphQLError(message=TASK_NOT_FOUND_MESSAGE)
        return True


schema = strawberry.Schema(
    query=TaskQuery,
    mutation=TaskMutation,
)

task_router_graphql = GraphQLRouter(
    schema=schema,
    context_getter=get_graphql_context,
)
