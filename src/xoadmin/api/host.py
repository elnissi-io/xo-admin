# src/xoadmin/host.py

from xoadmin.api.api import XOAPI


class HostManagement:
    def __init__(self, xo_api: XOAPI) -> None:
        self.xo_api = xo_api

    async def add_host(
        self,
        host: str,
        username: str,
        password: str,
        autoConnect: bool = True,
        allowUnauthorized: bool = False,
    ):
        """
        Registers a new Xen server.

        :param host: The host address of the new Xen server.
        :param username: Username for authentication with the Xen server.
        :param password: Password for authentication with the Xen server.
        :param autoConnect: Whether to automatically connect to the Xen server.
        :param allowUnauthorized: Whether to allow unauthorized certificates.
        """
        params = {
            "host": host,
            "username": username,
            "password": password,
            "autoConnect": autoConnect,
            "allowUnauthorized": allowUnauthorized,
        }

        # Ensure you're opening and closing the WebSocket connection appropriately.
        socket = self.xo_api.get_socket()
        await socket.open()
        result = await socket.call("server.add", params)
        await socket.close()
        return result

    async def list_hosts(self):
        """
        Retrieves a list of all registered Xen servers.

        :return: A list of dictionaries containing host information.
        """
        # Ensure you're opening and closing the WebSocket connection appropriately.
        socket = self.xo_api.get_socket()
        await socket.open()
        result = await socket.call("server.getAll", {})  # Empty params for all hosts
        await socket.close()
        return result

    async def delete_host(self, host_id: str):
        """
        Deletes a Xen server by its ID.

        :param host_id: The ID of the host to be deleted.
        """
        # Ensure you're opening and closing the WebSocket connection appropriately.
        socket = self.xo_api.get_socket()
        await socket.open()
        params = {"id": host_id}
        result = await socket.call("server.remove", params)
        await socket.close()
        return result
