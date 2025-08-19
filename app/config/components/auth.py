import pydantic
import pydantic_settings

class AuthConfig(pydantic_settings.BaseSettings):
    jwt_secret: str = pydantic.Field(default="supersecretkey")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30