import asyncio
from typing import Any

from xoadmin.api.api import XOAPI
from xoadmin.api.error import AuthenticationError, ServerError, XOSocketError
from xoadmin.api.host import HostManagement
from xoadmin.api.storage import StorageManagement
from xoadmin.api.user import UserManagement
from xoadmin.api.vm import VMManagement
from xoadmin.utils import get_logger

logger = get_logger(__name__)


class XOAManager:
    """
    A manager class for orchestrating interactions with the Xen Orchestra API,
    handling authentication, and managing resources.
    """

    def __init__(
        self,
        host: str,
        rest_base_url: str = None,
        ws_url: str = None,
        verify_ssl: bool = True,
    ):
        self.host = host
        self.verify_ssl = verify_ssl
        self.rest_base_url = self._sanitize_rest_base_url(rest_base_url, host)
        self.ws_url = self._sanitize_ws(ws_url)
        self.api = XOAPI(
            self.rest_base_url, ws_url=self.ws_url, verify_ssl=self.verify_ssl
        )
        # The management classes will be initialized after authentication
        self.user_management = None
        self.vm_management = None
        self.storage_management = None

    def _sanitize_rest_base_url(self, rest_base_url: str, host: str) -> str:
        """
        Sanitizes the REST base URL, ensuring it includes the protocol and default port.

        Parameters:
            rest_base_url (str): The REST base URL.
            host (str): The host address.
            verify_ssl (bool): Whether to verify SSL certificates.

        Returns:
            str: The sanitized REST base URL.
        """
        if not rest_base_url:
            protocol = "https" if self.verify_ssl else "http"
            return f"{protocol}://{host}"
        elif rest_base_url.startswith(("http://", "https://")):
            return rest_base_url
        else:
            raise ValueError("URL must start with http:// or https://")

    def _sanitize_ws(self, ws_url: str) -> str:
        """
        Sanitizes the WebSocket URL, ensuring it follows the correct format.

        Parameters:
            ws_url (str): The WebSocket URL or hostname.

        Returns:
            str: The sanitized WebSocket URL.
        """
        protocol = "wss" if self.verify_ssl else "ws"
        if not ws_url:
            return f"{protocol}://{self.host}"

        if "://" in ws_url:
            if ws_url.startswith(("ws://", "wss://", "http://", "https://")):
                # Replace http/https with appropriate WebSocket protocol
                ws_url = ws_url.replace("http://", "ws://").replace(
                    "https://", "wss://"
                )
                return ws_url  # URL already contains correct protocol
            else:
                raise ValueError(
                    "WebSocket URL must start with http://, https://, ws://, or wss://"
                )
        else:
            # If ws_url is a simple hostname or hostname:port
            return f"{protocol}://{ws_url}"

    def set_verify_ssl(self, enabled: bool) -> None:
        self.api.set_verify_ssl(enabled)
        self.verify_ssl = self.api.ws.verify_ssl
        logger.debug(
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
        logger.debug("Authenticated and ready to manage Xen Orchestra.")

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
    manager = XOAManager("localhost", "http://localhost:80", verify_ssl=False)
    await manager.authenticate(username="admin", password="password")
    vms = await manager.list_all_vms()
    print(vms)
    await manager.close()


if __name__ == "__main__":
    asyncio.run(main())
