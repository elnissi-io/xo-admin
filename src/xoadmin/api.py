import httpx
from typing import Any, Dict, Optional

# Assuming you've set up get_logger in .utils
from xoadmin.utils import get_logger
from xoadmin.websocket import Xo

logger = get_logger(__name__)

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
class XOApi:
    """An asynchronous client for interacting with Xen Orchestra's REST API."""

    def __init__(self, base_url: str, ws_url: str = None, credentials: Dict[str, str]=None, verify_ssl: bool = True) -> None:
        self.base_url = base_url
        self.session = httpx.AsyncClient(verify=verify_ssl, follow_redirects=True)
        self.auth_token = None
        # Initialize WebSocket connection for authentication
        self.ws_url= ws_url or "ws://localhost"
        self.credentials = credentials or {"email":"admin@admin.net","password":"admin"}
        self.ws = Xo(url=self.ws_url, verify_ssl=verify_ssl)

    async def authenticate_with_websocket(self,username:str,password:str) -> None:
        """Authenticate using WebSocket and retrieve token."""
        self.ws.set_credentials(username=username,password=password)
        await self.ws.open()
        if self.ws.user and 'authenticationToken' in self.ws.user:
            self.auth_token = self.ws.user['authenticationToken']
            logger.info("Successfully authenticated via WebSocket.")
        else:
            raise AuthenticationError("Failed to authenticate via WebSocket.")
        await self.ws.close()

    async def authenticate_with_credentials(self, username: str, password: str) -> None:
        """
        Authenticate using username and password to obtain authentication tokens.
        """
        raise NotImplementedError("Not supported yet, use XOApi.authenticate_with_websocket.")
        auth_url = f"{self.base_url}/rest/v0/auth/signin"
        headers = {'Accept': 'application/json'} 
        response = await self.session.post(auth_url, headers=headers,json={'username': username, 'password': password})
        logger.info(f"Response text: {response.text}")
        if response.status_code == 200:
            # Extract session and CSRF tokens from response cookies
            data = response.json()
            self.auth_token = data.get('authenticationToken')
            if not self.auth_token:
                raise AuthenticationError("Failed to obtain authentication token.")

            logger.info("Successfully authenticated.")
        else:
            raise AuthenticationError(f"Failed to authenticate: {response.text}")


    async def close(self) -> None:
        """Close the session."""
        await self.session.aclose()
    async def _refresh_token(self) -> None:
        """Refresh the authentication token."""
        # TODO:IMPLEMENT
        logger.info("Token refreshed.")

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """A wrapper for making authenticated requests with token refresh logic."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Cookie": f"authenticationToken={self.auth_token}"}
        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status_code == 401:
                await self._refresh_token()  # Refresh token and retry once
                headers["Cookie"] = f"authenticationToken={self.auth_token}"
                async with self.session.request(method, url, headers=headers, **kwargs) as retry_response:
                    retry_response.raise_for_status()
                    return retry_response.json()
            response.raise_for_status()
            return response.json()

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any) -> Any:
        return await self._request("POST", endpoint, json=json_data, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> bool:
        await self._request("DELETE", endpoint, **kwargs)
        return True

    async def patch(self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any) -> Any:
        return await self._request("PATCH", endpoint, json=json_data, **kwargs)
