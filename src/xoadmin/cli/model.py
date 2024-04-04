import os
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class XOASettings:
    __prefix__ = "xoa."
    host: str = "XOA_HOST"
    rest_api: str = "XOA_REST_API"
    websocket: str = "XOA_WEBSOCKET"
    username: str = "XOA_USERNAME"
    password: str = "XOA_PASSWORD"
    verify_ssl: str = "XOA_VERIFY_SSL"

    defaults = {
        "host": "default_host",
        "websocket": "default_websocket",
        "rest_api": "default_rest_api",
        "username": "default_username",
        "password": "default_password",
        "verify_ssl": False,
    }

    @staticmethod
    def get_env_var_name(key: str) -> Optional[str]:
        """Return the environment variable name for a given key."""
        name = getattr(XOASettings, key, None)
        return name

    @staticmethod
    def get(key: str) -> Optional[str]:
        """Return the value of the environment variable for a given key."""
        env_var_name = XOASettings.get_env_var_name(key)
        if env_var_name:
            return os.getenv(env_var_name)
        return None

    @staticmethod
    def get_key_for_env_var(env_var_name: str) -> Optional[str]:
        """Return the key in XOASettings corresponding to a given environment variable name."""
        for key, value in XOASettings.__dict__.items():
            if value == env_var_name and not key.startswith("__"):
                return key
        return None


class XOA(BaseModel):
    host: str
    websocket: Optional[str] = None
    rest_api: Optional[str] = None
    username: str
    password: SecretStr
    verify_ssl: bool = True

    model_config = ConfigDict(extra="allow")


class XOAConfig(BaseModel):
    xoa: XOA

    model_config = ConfigDict(extra="allow")
