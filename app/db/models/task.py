from fastapi_babel import _

from tortoise import fields
from tortoise.fields.base import OnDelete

from db.models.base import BaseModel
from services.enums import TranslatableStrEnum

class Task(BaseModel):
    """Represent Task in db."""

    id = fields.UUIDField(
        pk=True,
    )
    title = fields.CharField(
        max_length=120,
    )
    description = fields.TextField(
        max_length=500,
        null=True,
    )
    class StatusChoices(TranslatableStrEnum):
        """String based enum for task statuses."""

        CREATED = ("Created", _("Created"))
        IN_PROGRESS = ("In progress", _("In progress"))
        COMPLETE = ("Complete", _("Complete"))
    status = fields.CharEnumField(
        enum_type=StatusChoices,
        default=StatusChoices.CREATED,
    )
    user = fields.ForeignKeyField(
        model_name="server.User",
        related_name="tasks",
        on_delete=OnDelete.CASCADE,
    )
