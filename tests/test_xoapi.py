import pytest
from httpx import Response

from xoadmin.api.api import XOAPI
from xoadmin.api.websocket import XOSocket


@pytest.mark.asyncio
async def test_authenticate_with_websocket(mocker):
    mock_open = mocker.patch.object(XOSocket, "open", return_value=None)
    mock_create_token = mocker.patch.object(
        XOSocket, "create_token", return_value="test_token"
    )
    mock_close = mocker.patch.object(XOSocket, "close", return_value=None)

    xoapi = XOAPI(base_url="http://test", ws_url="ws://test", verify_ssl=False)
    await xoapi.authenticate_with_websocket("test_user", "test_pass")

    mock_open.assert_called_once()
    mock_create_token.assert_called_once_with(description="xoadmin token")
    mock_close.assert_called_once()
    assert xoapi.auth_token == "test_token"
