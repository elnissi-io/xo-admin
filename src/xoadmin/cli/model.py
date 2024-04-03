from pydantic import BaseModel, Field, SecretStr

ENV_VARIABLE_MAPPING = {
    "host": "XOA_HOST",
    "username": "XOA_USERNAME",
    "password": "XOA_PASSWORD",
}


class XOA(BaseModel):
    host: str = Field(..., alias="host", env="XOA_HOST")
    username: str = Field(..., alias="username", env="XOA_USERNAME")
    password: SecretStr = Field(..., alias="password", env="XOA_PASSWORD")

    class Config:
        extra = "allow"


class XOAConfig(BaseModel):
    xoa: XOA

    class Config:
        extra = "allow"
