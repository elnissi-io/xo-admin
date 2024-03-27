import asyncio
import json
import ssl
import websockets
from uuid import uuid4
from xoadmin.utils import get_logger
from typing import Dict
import traceback
import uuid
logger = get_logger()

class XoSocketError(Exception):
    """Exception raised for errors encountered within the Xo class."""

class XoSocket:
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
  
    async def open(self)-> bool:
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
                await self.sign_in(self.credentials)
                logger.info("Sign in successful.")
        except Exception as e:
            logger.error(f"Error opening WebSocket connection: {e}")
            raise
        
        return True
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
            raise XoSocketError("session.*() methods are disabled from this interface, except session.signIn")
        
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
        response = await self.call('session.signIn', credentials)
        if 'result' in response and 'authenticationToken' in response['result']:
            self.user = response['result']
            logger.info("Signed in as:", self.user)
        elif 'error' in response:
            raise XoSocketError(f"Failed to sign in: {response['error']}")
        
    async def create_token(self, description="xoadmin token"):
            """
            Creates an authentication token, including client information.
            """
            # Generate a simple client ID or use more complex logic as needed
            client_id = str(uuid.uuid4())
            client_info = {"id": client_id}
            params = {
                "description": description,
                "client": client_info,
            }
            response = await self.call('token.create', params)
            if 'result' in response:
                token_id = response['result']
                logger.info(f"Token created successfully: {token_id}")
                return token_id
            else:
                error_msg = response.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Failed to create token: {error_msg}")
                raise XoSocketError(f"Failed to create token: {error_msg}")

# Example Usage
# async def main():
#     xo = XoSocket(url="ws://localhost:80", credentials={"email": "admin", "password": "password"}, verify_ssl=False)
#     await xo.open()
#     # Assuming successful authentication has occurred
#     try:
#         token_id = await xo.create_token(description="My API Token")
#         logger.info(f"Token created successfully: {token_id}")
#         # Store or use the token_id as needed for authenticated API interactions
#     except Exception as e:
#         logger.error(f"{e}")
#     await xo.close()

# if __name__ == "__main__":
#     asyncio.run(main())