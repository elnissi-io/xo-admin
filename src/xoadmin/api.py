import httpx
from typing import Any, Dict, Optional

# Assuming you've set up get_logger in .utils
from xoadmin.utils import get_logger
from xoadmin.websocket import XoSocket

logger = get_logger(__name__)

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
class XOAPI:
    """An asynchronous client for interacting with Xen Orchestra's REST API."""

    def __init__(self, base_url: str, ws_url: str = None, credentials: Dict[str, str]=None, verify_ssl: bool = True) -> None:
        self.base_url = base_url
        self.session = httpx.AsyncClient(verify=verify_ssl, follow_redirects=True)
        self.auth_token = None
        # Initialize WebSocket connection for authentication
        self.ws_url= ws_url or "ws://localhost"
        self.credentials = credentials or {"email":"admin@admin.net","password":"admin"}
        self.ws = XoSocket(url=self.ws_url, verify_ssl=verify_ssl)
    
    def verify_ssl(self,enabled:bool):
        self.ws = XoSocket(url=self.ws_url, verify_ssl=enabled)

    def set_credentials(self,username:str,password:str):
        self.credentials={"email":str(username),"password":str(password)}
        self.ws.set_credentials(username=username,password=password)

    async def authenticate_with_websocket(self, username: str, password: str) -> None:
        self.set_credentials(username=username,password=password)
        await self.ws.open()
        
        try:
            self.auth_token = await self.ws.create_token(description="xoadmin token")
        except Exception as e:
            raise AuthenticationError("Failed to authenticate via WebSocket.")
        
        await self.ws.close()


    async def authenticate_with_credentials(self, username: str, password: str) -> None:
        """
        Authenticate using username and password to obtain authentication tokens.
        """
        raise NotImplementedError("Not supported yet, use XOAPI.authenticate_with_websocket.")

    async def close(self) -> None:
        """Close the session."""
        await self.session.aclose()

    async def _refresh_token(self) -> None:
        """Refreshes the authentication token using stored credentials."""
        if not self.credentials:
            logger.error("No credentials stored for refreshing the token.")
            raise AuthenticationError("Unable to refresh token due to missing credentials.")
        await self.authenticate_with_websocket(self.credentials['email'], self.credentials['password'])
        logger.info("Authentication token refreshed.")

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """Sends a request, attempting a token refresh on 401 responses."""
        headers = {"Authorization": f"Bearer {self.auth_token}"}  # Adjust based on actual auth header
        response = await self.session.request(method, f"{self.base_url}/{endpoint}", headers=headers, **kwargs)
        if response.status_code == 401:
            await self._refresh_token()
            headers["Authorization"] = f"Bearer {self.auth_token}"
            response = await self.session.request(method, f"{self.base_url}/{endpoint}", headers=headers, **kwargs)
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
