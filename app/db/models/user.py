from tortoise import fields

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
