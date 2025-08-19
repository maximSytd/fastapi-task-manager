import pydantic

class UserBase(pydantic.BaseModel):
    """Base User schema."""

    username: str


class UserCreate(UserBase):
    """User schema to create instance."""

    password: str


class UserOut(UserBase):
    """User schema for db instances."""

    id: int

    class Config:
        from_attributes = True
