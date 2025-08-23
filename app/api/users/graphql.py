import strawberry
from strawberry.fastapi import GraphQLRouter
from tortoise.exceptions import IntegrityError
from strawberry.exceptions import StrawberryGraphQLError

from db.models import User
from db.graphql import UserType, TokenType
from services.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
)
from .messages import (
    INCORRECT_CREDENTIALS_MESSAGE,
    USERNAME_ALREADY_EXIST_MESSAGE,
)


@strawberry.type
class Query:
    """GraphQL queries."""

    @strawberry.field
    async def user(self, id: int) -> UserType:
        """Get user by ID."""
        return await User.get_or_none(id=id)


@strawberry.type
class UserMutation:
    """GraphQL mutations for User type."""

    @strawberry.mutation
    async def register(self, username: str, password: str) -> UserType:
        """Return and register new user."""
        try:
            user = await User.create(
                username=username,
                password_hash=get_password_hash(password),
            )
        except IntegrityError:
            raise StrawberryGraphQLError(
                message=USERNAME_ALREADY_EXIST_MESSAGE,
            )
        return user

    @strawberry.mutation
    async def login(self, username: str, password: str) -> TokenType:
        """Return auth token and validate credentials."""
        user = await User.get_or_none(username=username)
        if not user or not verify_password(
            plain_password=password,
            hashed_password=user.password_hash,
        ):
            return StrawberryGraphQLError(
                message=INCORRECT_CREDENTIALS_MESSAGE,
            )
        return TokenType(
            access_token=create_access_token(
                data={
                    "sub": user.username,
                },
            ),
            token_type="bearer",
        )

schema=strawberry.Schema(
    query=Query,
    mutation=UserMutation,
)

user_router_graphql = GraphQLRouter(schema=schema)
