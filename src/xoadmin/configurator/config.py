# Assuming these models exist in xoa_container/models/config.py or similar

from pydantic import BaseModel
from typing import List, Optional

class HypervisorConfig(BaseModel):
    host: str
    username: str
    password: str
    autoConnect: Optional[bool] = True
    allowUnauthorized: Optional[bool] = False

class XOAInstance(BaseModel):
    host: str
    username: str 
    password: str
class UserConfig(BaseModel):
    username: str
    password: str
    permission: Optional[str] = "none"
class AppConfig(BaseModel):
    xoa: XOAInstance
    hypervisors: List[HypervisorConfig]
    users: List[UserConfig]