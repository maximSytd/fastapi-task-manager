import pydantic


class Token(pydantic.BaseModel):
    """OAuth Token schema."""
    access_token: str
    token_type: str

class UserLogin(pydantic.BaseModel):
    """User login schema."""

    username: str
    password: str