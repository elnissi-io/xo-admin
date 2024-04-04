from typing import Any, Dict, Optional

import httpx

from xoadmin.api.websocket import XOSocket

# Assuming you've set up get_logger in .utils
from xoadmin.utils import get_logger

logger = get_logger(__name__)


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""


class XOAPI:
    """An asynchronous client for interacting with Xen Orchestra's REST API."""

    def __init__(
        self,
        rest_base_url: str,
        ws_url: str = None,
        credentials: Dict[str, str] = None,
        verify_ssl: bool = True,
    ) -> None:
        self.verify_ssl = verify_ssl
        self.rest_base_url = rest_base_url
        self.session = httpx.AsyncClient(verify=verify_ssl, follow_redirects=True)
        self.auth_token = None
        # Initialize WebSocket connection for authentication
        self.ws_url = ws_url or "ws://localhost"
        self.credentials = credentials or {
            "email": "admin@admin.net",
            "password": "admin",
        }
        self.ws = XOSocket(url=self.ws_url, verify_ssl=verify_ssl)

    def get_socket(self) -> XOSocket:
        return self.ws

    def set_verify_ssl(self, enabled: bool):
        self.ws = XOSocket(url=self.ws_url, verify_ssl=enabled)
        self.verify_ssl = self.ws.verify_ssl

    def set_credentials(self, username: str, password: str):
        self.credentials = {"email": str(username), "password": str(password)}
        self.ws.set_credentials(username=username, password=password)

    async def authenticate_with_websocket(self, username: str, password: str) -> None:
        self.set_credentials(username=username, password=password)
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
        raise NotImplementedError(
            "Not supported yet, use XOAPI.authenticate_with_websocket."
        )

    async def close(self) -> None:
        """Close the session."""
        await self.session.aclose()

    async def _refresh_token(self) -> None:
        """Refreshes the authentication token using stored credentials."""
        if not self.credentials:
            logger.error("No credentials stored for refreshing the token.")
            raise AuthenticationError(
                "Unable to refresh token due to missing credentials."
            )
        await self.authenticate_with_websocket(
            self.credentials["email"], self.credentials["password"]
        )
        logger.debug("Authentication token refreshed.")

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        # Prepare the URL
        url = f"{self.rest_base_url}/{endpoint}"
        # Ensure cookies are correctly set for the session
        if self.auth_token:
            self.session.cookies.set("authenticationToken", self.auth_token)
        else:
            logger.error("No authentication token available.")
            raise AuthenticationError("Authentication required.")
        # Make the request
        response = await self.session.request(method, url, **kwargs)
        # Check for 401 Unauthorized response and attempt to refresh the token
        if response.status_code == 401:
            logger.warning(
                f"Received 401 Unauthorized for {endpoint}, attempting token refresh."
            )
            await self._refresh_token()
            # Retry the request after refreshing the token
            response = await self.session.request(method, url, **kwargs)

        # Check for successful response
        response.raise_for_status()
        return response.json()

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(
        self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any
    ) -> Any:
        return await self._request("POST", endpoint, json=json_data, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> bool:
        await self._request("DELETE", endpoint, **kwargs)
        return True

    async def patch(
        self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any
    ) -> Any:
        return await self._request("PATCH", endpoint, json=json_data, **kwargs)
