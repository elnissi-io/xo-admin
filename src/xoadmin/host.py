# src/xoadmin/host.py

from xoadmin.api import XOAPI


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
