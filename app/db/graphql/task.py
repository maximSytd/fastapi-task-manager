import uuid
import datetime

import strawberry

@strawberry.type
class StatusType:
    """Graphql Task status type."""

    value: str
    label: str


@strawberry.type
class TaskType:
    """GraphQL Task type."""

    id: uuid.UUID
    title: str
    description: str | None = None
    status: StatusType
    created: datetime.datetime
    modified: datetime.datetime


@strawberry.input
class TaskCreateInput:
    """GraphQL Task create input type."""

    title: str
    description: str | None = None


@strawberry.input
class TaskUpdateInput:
    """GraphQL Task update input type."""

    title: str | None = None
    description: str | None = None
    status: str | None = None
