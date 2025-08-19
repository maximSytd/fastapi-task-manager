import pydantic


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str

class UserLogin(pydantic.BaseModel):
    username: str
    password: str