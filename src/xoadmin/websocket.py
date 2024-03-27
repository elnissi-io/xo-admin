import asyncio
import json
import ssl
import websockets
from uuid import uuid4
from xoadmin.utils import get_logger
from typing import Dict

logger = get_logger()

class XoError(Exception):
    """Exception raised for errors encountered within the Xo class."""

class Xo:
    """
    A client for establishing a WebSocket connection with a Xen Orchestra server
    and performing JSON-RPC calls over this connection.
    """
    def __init__(self, url: str, credentials: Dict[str,str] = None, verify_ssl: bool = True):
        """
        Initializes the Xo client with connection details.
        
        :param url: The WebSocket URL of the Xen Orchestra server.
        :param credentials: A dictionary containing login credentials, specifically
                            'email' and 'password'.
        :param verify_ssl: A flag to specify if SSL certificates should be verified.
                           Set to False to allow self-signed certificates.
        """
        self.url = f"{url.rstrip('/')}/api/"
        self.credentials = credentials
        self.user = None
        self.websocket = None
        self.verify_ssl = verify_ssl
        
    def set_credentials(self,username:str, password:str)->None:
        self.credentials = {"email": str(username), "password": str(password)}
  
    async def open(self):
        """
        Opens the WebSocket connection and signs in with the provided credentials.
        """
        ssl_context = ssl.create_default_context() if self.url.startswith("wss://") and self.verify_ssl else None
        if ssl_context and not self.verify_ssl:
            # Customize the SSL context for self-signed certificates
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        try:
            self.websocket = await websockets.connect(self.url, ssl=ssl_context if self.url.startswith("wss://") else None)
            logger.info("Connection opened.")
            if self.credentials:
                logger.info(f"{self.credentials}")
                await self.sign_in(self.credentials)
        except Exception as e:
            logger.error(f"Error opening WebSocket connection: {e}")
            raise
    async def close(self):
        """
        Closes the WebSocket connection.
        """
        await self.websocket.close()
        logger.info("Connection closed.")

    async def call(self, method: str, params: dict = None):
        """
        Performs a JSON-RPC call over the WebSocket connection.
        
        :param method: The JSON-RPC method name to call.
        :param params: A dictionary of parameters to pass with the method call.
        :return: The JSON-RPC response from the server.
        :raises XoError: If the method is not allowed or if other errors occur.
        """
        # Allow session.signIn method, but block other session.* methods
        if method.startswith('session.') and method != 'session.signIn':
            raise XoError("session.*() methods are disabled from this interface, except session.signIn")
        
        if params is None:
            params = {}
        
        message = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(uuid4())
        })
        await self.websocket.send(message)
        response = await self.websocket.recv()
        response_data = json.loads(response)
        return response_data

    async def sign_in(self, credentials: dict):
        """
        Signs into the Xen Orchestra server using the provided credentials.
        
        :param credentials: A dictionary containing login credentials, specifically
                            'email' and 'password'.
        :raises XoError: If sign-in fails.
        """
        response = await self.call('session.signIn', credentials)
        if 'result' in response:
            self.user = response['result']
            logger.info("Signed in as:", self.user)
        elif 'error' in response:
            raise XoError(f"Failed to sign in: {response['error']}")
# Example Usage
async def main():
    xo = Xo(url="wss://localhost:443", credentials={"email": "admin@admin.net", "password": "admin"}, verify_ssl=False)
    await xo.open()
    # Perform calls
    try:
        result = await xo.call('acl.get', {})
        logger.info("Success:", result)
    except Exception as e:
        logger.error("Failure:", e)
    await xo.close()

if __name__ == "__main__":
    asyncio.run(main())
