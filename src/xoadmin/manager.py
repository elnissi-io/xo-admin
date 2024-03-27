import asyncio
from typing import Any

from xoadmin.api import XOAPI
from xoadmin.user import UserManagement
from xoadmin.vm import VMManagement
from xoadmin.storage import StorageManagement
from xoadmin.utils import get_logger

logger = get_logger(__name__)

class XOAManager:
    """
    A manager class for orchestrating interactions with the Xen Orchestra API,
    handling authentication, and managing resources.
    """
    
    def __init__(self, base_url: str,verify_ssl:bool=True):
        self.base_url = base_url
        self.api = XOAPI(self.base_url,verify_ssl=verify_ssl)
        # The management classes will be initialized after authentication
        self.user_management = None
        self.vm_management = None
        self.storage_management = None
        
    def verify_ssl(self,enabled:bool) -> None:
        self.api.verify_ssl(enabled)
        logger.info(f"SSL verification {'enabled' if enabled else 'disabled'}.")
        
    async def authenticate(self, username: str, password: str) -> None:
        """
        Authenticates with the Xen Orchestra API using the provided credentials
        and initializes the management classes.
        """
        await self.api.authenticate_with_websocket(username, password)

        # Initialize management classes with the authenticated API instance
        self.user_management = UserManagement(self.api)
        self.vm_management = VMManagement(self.api)
        self.storage_management = StorageManagement(self.api)

        logger.info("Authenticated and ready to manage Xen Orchestra.")

    async def create_user(self, email: str, password: str, permission: str = "none") -> Any:
        """
        Creates a new user with the specified email, password, and permission level."""
        # Directly use the method from UserManagement
        return await self.user_management.create_user(email, password, permission)

    async def delete_user(self, user_email: str) -> bool:
        """
        Deletes a user by email.
        """
        users = await self.user_management.list_users()
        user = next((user for user in users if user['email'] == user_email), None)
        if user:
            return await self.user_management.delete_user(user['id'])
        logger.warning(f"User {user_email} not found.")
        return False
    
    async def list_all_vms(self) -> Any:
        """
        Lists all VMs.
        """
        return await self.vm_management.list_vms()

    async def create_vdi(self, sr_id: str, size: int, name_label: str) -> Any:
        """
        Creates a new VDI on the specified SR.
        """
        return await self.storage_management.create_vdi(sr_id, size, name_label)

    async def close(self) -> None:
        """
        Closes the session.
        """
        await self.api.close()

# Example usage
async def main():
    manager = XOAManager("http://localhost:80",verify_ssl=False)
    await manager.authenticate(username="admin",password="password")
    vms = await manager.list_all_vms()
    print(vms)
    await manager.close()

if __name__ == "__main__":
    asyncio.run(main())
