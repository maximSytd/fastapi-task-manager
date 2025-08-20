import factory
from async_factory_boy.factory.tortoise import AsyncTortoiseFactory

from db.models import User
from services.auth import get_password_hash

DEFAULT_PASSWORD = "TEST!!!"


class AsyncUserFactory(AsyncTortoiseFactory):
    """Async factory to generate test User instance."""

    username = factory.Faker("user_name")
    password_hash = factory.LazyFunction(
        lambda: get_password_hash(
            DEFAULT_PASSWORD,
        ),
    )

    class Meta:
        model = User

