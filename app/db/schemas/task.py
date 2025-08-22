import uuid
import typing
import datetime

import pydantic

from db.models import Task
from services.enums import StrEnumAsDict

class TaskBase(pydantic.BaseModel):
    """Base Task schema."""

    title: str
    description: None | str = None


class TaskCreate(TaskBase):
    """Task schema to create instance."""


class TaskUpdate(TaskBase):
    """Task schema to update instance."""

    title: None | str = None
    status: None | Task.StatusChoices = None


class TaskOut(TaskBase):
    """Task schema for db instances."""

    model_config = pydantic.ConfigDict(
        from_attributes = True
    )
    id: uuid.UUID
    status: StrEnumAsDict
    created: datetime.datetime
    modified: datetime.datetime

    @pydantic.field_validator("status", mode="before")
    @classmethod
    def convert_enum_to_dict(
        cls,
        value: typing.Any,
    ) -> typing.Any | StrEnumAsDict:
        """Return and convert enum into dict with value and label."""
        if isinstance(value, Task.StatusChoices):
            return value.as_dict()
        return value
