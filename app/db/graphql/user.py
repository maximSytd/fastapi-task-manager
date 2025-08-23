import datetime

import strawberry

@strawberry.type
class UserType:
    """GraphQL user type."""

    id: int | None
    username: str | None
    created: datetime.datetime
    modified: datetime.datetime


@strawberry.type
class TokenType:
    """GraphQL Token type."""

    access_token: str | None
    token_type: str | None
