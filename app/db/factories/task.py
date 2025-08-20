import factory
import factory.fuzzy
from async_factory_boy.factory.tortoise import AsyncTortoiseFactory

from db.models import Task
from db.factories import AsyncUserFactory


class AsyncTaskFactory(AsyncTortoiseFactory):
    """Async factory to generate test Task instance."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    status = factory.fuzzy.FuzzyChoice(Task.StatusChoices.values())
    user = factory.SubFactory(AsyncUserFactory)

    class Meta:
        model = Task
