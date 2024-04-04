from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, SecretStr

ENV_VARIABLE_MAPPING = {
    "__prefix__": "xoa.",
    "host": "XOA_HOST",
    "rest_api": "XOA_REST_API",
    "websocket": "XOA_WEBSOCKET",
    "username": "XOA_USERNAME",
    "password": "XOA_PASSWORD",
    "verify_ssl": "XOA_VERIFY_SSL",
}


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
