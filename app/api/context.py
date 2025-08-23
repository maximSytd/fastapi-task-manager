from fastapi import Request, Depends

from dependencies.auth import get_current_user
from db.models import User


async def get_graphql_context(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Custom graphql context handler with user."""
    return {"request": request, "user": current_user}
