import pydantic

class UserBase(pydantic.BaseModel):
    """Base User schema."""

    username: str


class UserCreate(UserBase):
    """User schema to create instance."""

    password: str


class UserOut(UserBase):
    """User schema for db instances."""

    model_config = pydantic.ConfigDict(
        from_attributes = True,
    )
    id: int
