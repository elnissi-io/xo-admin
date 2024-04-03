import asyncio
from typing import Any

from xoadmin.api.api import XOAPI
from xoadmin.api.error import AuthenticationError, ServerError, XOSocketError
from xoadmin.api.host import HostManagement
from xoadmin.api.storage import StorageManagement
from xoadmin.api.user import UserManagement
from xoadmin.utils import get_logger
from xoadmin.api.vm import VMManagement

logger = get_logger(__name__)


class XOAManager:
    """
    A manager class for orchestrating interactions with the Xen Orchestra API,
    handling authentication, and managing resources.
    """

    def __init__(self, base_url: str, verify_ssl: bool = True):
        self.base_url = base_url
        self.ws_url = self._convert_http_to_ws(base_url)
        self.api = XOAPI(self.base_url, ws_url=self.ws_url, verify_ssl=verify_ssl)
        # The management classes will be initialized after authentication
        self.user_management = None
        self.vm_management = None
        self.storage_management = None

    def _convert_http_to_ws(self, url: str) -> str:
        """
        Converts an HTTP or HTTPS URL to its WebSocket equivalent (WS or WSS).

        Parameters:
            url (str): The HTTP or HTTPS URL.

        Returns:
            str: The converted WS or WSS URL.
        """
        if url.startswith("https://"):
            return url.replace("https://", "wss://", 1)
        elif url.startswith("http://"):
            return url.replace("http://", "ws://", 1)
        else:
            raise ValueError("URL must start with http:// or https://")

    def verify_ssl(self, enabled: bool) -> None:
        self.api.verify_ssl(enabled)
        logger.info(
            f"SSL verification {'enabled' if self.api.ws.verify_ssl else 'disabled'}."
        )

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
        self.host_management = HostManagement(self.api)
        logger.info("Authenticated and ready to manage Xen Orchestra.")

    async def create_user(
        self, email: str, password: str, permission: str = "none"
    ) -> Any:
        """
        Creates a new user with the specified email, password, and permission level."""
        # Directly use the method from UserManagement
        await self.user_management.create_user(email, password, permission)
        logger.info(f"User {email} created successfully.")

    async def delete_user(self, user_email: str) -> bool:
        """
        Deletes a user by email.
        """
        users = await self.user_management.list_users()
        user = next((user for user in users if user["email"] == user_email), None)
        if user:
            return await self.user_management.delete_user(user["id"])
        logger.warning(f"User {user_email} not found.")
        return False

    async def add_host(
        self,
        host: str,
        username: str,
        password: str,
        autoConnect: bool = True,
        allowUnauthorized: bool = False,
    ):
        try:
            result = await self.host_management.add_host(
                host=host,
                username=username,
                password=password,
                autoConnect=autoConnect,
                allowUnauthorized=allowUnauthorized,
            )
            logger.info(f"Host {host} added successfully.")
        except XOSocketError as e:
            # Now, we can decide how to handle the error based on its message
            if "server already exists" in str(e):
                logger.error(f"Cannot add host {host}: The server already exists.")
            elif "authentication failed" in str(e):
                logger.error(f"Cannot add host {host}: Authentication failed.")
            else:
                logger.error(f"Failed to add host {host}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while adding host {host}: {e}")

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
    manager = XOAManager("http://localhost:80", verify_ssl=False)
    await manager.authenticate(username="admin", password="password")
    vms = await manager.list_all_vms()
    print(vms)
    await manager.close()


if __name__ == "__main__":
    asyncio.run(main())
