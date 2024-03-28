# src/xoadmin/host.py

from xoadmin.api import XOAPI


class HostManagement:
    def __init__(self, xo_api: XOAPI) -> None:
        self.xo_api = xo_api

    async def add_host(self, params: dict):
        """
        Registers a new Xen server.

        :param host_details: A dictionary containing the details of the host to add.
        """
        socket = self.xo_api.get_socket()
        await socket.open()
        result = await self.xo_api.get_socket().call("server.add", params)
        await socket.close()
        return result
