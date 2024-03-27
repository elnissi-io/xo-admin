import httpx
from typing import Any, Dict, Optional

# Assuming you've set up get_logger in .utils
from .utils import get_logger

logger = get_logger(__name__)

class XOApi:
    """An asynchronous client for interacting with Xen Orchestra's REST API."""

    def __init__(self, base_url: str, auth_token: str) -> None:
        self.base_url: str = base_url
        self.session: httpx.AsyncClient = httpx.AsyncClient()
        self.session.headers['Cookie'] = f'authenticationToken={auth_token}'

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Asynchronously send a GET request to the specified endpoint."""
        async with self.session.get(f'{self.base_url}/{endpoint}', params=params) as response:
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any) -> Any:
        """Asynchronously send a POST request to the specified endpoint."""
        async with self.session.post(f'{self.base_url}/{endpoint}', json=json_data, **kwargs) as response:
            response.raise_for_status()
            return response.json()

    async def delete(self, endpoint: str, **kwargs: Any) -> bool:
        """Asynchronously send a DELETE request to the specified endpoint."""
        async with self.session.delete(f'{self.base_url}/{endpoint}', **kwargs) as response:
            response.raise_for_status()
            return response.status_code == 204

    async def patch(self, endpoint: str, json_data: Dict[str, Any], **kwargs: Any) -> Any:
        """Asynchronously send a PATCH request to the specified endpoint."""
        async with self.session.patch(f'{self.base_url}/{endpoint}', json=json_data, **kwargs) as response:
            response.raise_for_status()
            return response.json()
    
    async def close(self) -> None:
        """Close the session."""
        await self.session.aclose()
