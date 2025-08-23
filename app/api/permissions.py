from strawberry.types import Info
from strawberry.permission import BasePermission


UNAUTHENTICATED_MESSAGE = "Authentication required"


class IsAuthenticated(BasePermission):
    """Class based permission for graphql queries."""

    message = UNAUTHENTICATED_MESSAGE

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        """Return bool and verify user's permission."""
        return bool(info.context.get("user"))
