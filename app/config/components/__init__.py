from config.components.base import BaseConfig
from config.components.db import DatabaseConfig
from config.components.auth import AuthConfig


class ComponentsConfig(BaseConfig, DatabaseConfig, AuthConfig):
    pass


__all__ = ["ComponentsConfig"]