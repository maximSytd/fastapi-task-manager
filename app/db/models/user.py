from tortoise import fields
from tortoise.fields.base import OnDelete

from db.models.base import BaseModel

class User(BaseModel):
    """Represent User in db."""

    username = fields.CharField(
        max_length=64,
        unique=True,
    )
    password_hash = fields.CharField(
        max_length=128,
    )
    grade = fields.ForeignKeyField(
        model_name="server.Grade",
        related_name="users",
        on_delete=OnDelete.SET_NULL,
        null=True,
    )
    is_admin = fields.BooleanField(
        default=False,
    )
