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
    def get(key: str) -> Optional[str]:
        return getattr(XOASettings, key, None)

    @staticmethod
    def get_env_key(key: str) -> Optional[str]:
        return os.getenv(getattr(XOASettings, key, None))

    @staticmethod
    def get_key(env_key: str) -> str:
        """
        Get the key corresponding to the given environment variable.
        """
        for key, value in XOASettings.__annotations__.items():
            if value == env_key:
                return key
        raise KeyError(f"No key found for environment variable: {env_key}")


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
