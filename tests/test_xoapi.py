from unittest.mock import patch

import pytest
from httpx import Response

from xoadmin.api.api import XOAPI
from xoadmin.api.error import AuthenticationError, ServerError, XOSocketError
from xoadmin.api.host import HostManagement
from xoadmin.api.manager import XOAManager
from xoadmin.api.user import UserManagement
from xoadmin.api.websocket import XOSocket


@pytest.mark.asyncio
async def test_authenticate_with_websocket(mocker):
    mock_open = mocker.patch.object(XOSocket, "open", return_value=None)
    mock_create_token = mocker.patch.object(
        XOSocket, "create_token", return_value="test_token"
    )
    mock_close = mocker.patch.object(XOSocket, "close", return_value=None)

    xoapi = XOAPI(rest_base_url="http://test", ws_url="ws://test", verify_ssl=False)
    await xoapi.authenticate_with_websocket("test_user", "test_pass")

    mock_open.assert_called_once()
    mock_create_token.assert_called_once_with(description="xoadmin token")
    mock_close.assert_called_once()
    assert xoapi.auth_token == "test_token"


def test_sanitize_ws():
    # Test case when SSL verification is enabled (default)
    manager = XOAManager("localhost", verify_ssl=True)
    assert manager._sanitize_ws("localhost") == "wss://localhost"

    # Test case when SSL verification is disabled
    manager = XOAManager("localhost", verify_ssl=False)
    assert manager._sanitize_ws("localhost") == "ws://localhost"

    # Additional test case for HTTPS with default port (443)
    manager = XOAManager("localhost", verify_ssl=True)
    assert manager._sanitize_ws("localhost") == "wss://localhost"

    # Test case for HTTPS with non-default port
    manager = XOAManager("localhost", verify_ssl=True)
    assert manager._sanitize_ws("localhost:8443") == "wss://localhost:8443"

    # Test case for HTTP with non-default port
    manager = XOAManager("localhost", verify_ssl=False)
    assert manager._sanitize_ws("localhost:8080") == "ws://localhost:8080"

    # Test case for invalid URL
    with pytest.raises(ValueError):
        manager._sanitize_ws("ftp://localhost:21")


@pytest.mark.asyncio
async def test_verify_ssl(mocker):
    # Mock only the verify_ssl method to keep other parts of the __init__ intact.
    mock_verify_ssl = mocker.patch.object(XOAPI, "verify_ssl")
    manager = XOAManager("http://test", verify_ssl=False)
    manager.api = XOAPI("http://test", "ws://test")
    manager.api.ws = mocker.Mock()  # Mock the ws attribute directly
    manager.set_verify_ssl(True)
    mock_verify_ssl.assert_called_with(True)


@pytest.mark.asyncio
async def test_authenticate_error_handling(mocker):
    mocker.patch.object(XOAPI, "__init__", return_value=None)
    mock_authenticate = mocker.patch.object(
        XOAPI, "authenticate_with_websocket", side_effect=AuthenticationError
    )
    manager = XOAManager("http://test", verify_ssl=False)
    manager.api = XOAPI("http://test")

    with pytest.raises(AuthenticationError):
        await manager.authenticate("user", "pass")
    mock_authenticate.assert_called()


@pytest.mark.asyncio
async def test_create_and_delete_user(mocker):
    mocker.patch.object(UserManagement, "create_user", return_value=True)
    mocker.patch.object(
        UserManagement,
        "list_users",
        return_value=[{"email": "test@test.com", "id": "1"}],
    )
    mocker.patch.object(UserManagement, "delete_user", return_value=True)

    manager = XOAManager("http://test")
    manager.user_management = UserManagement(XOAPI("http://test"))

    # Test create user
    await manager.create_user("test@test.com", "password")
    manager.user_management.create_user.assert_called_with(
        "test@test.com", "password", "none"
    )

    # Test delete user
    result = await manager.delete_user("test@test.com")
    assert result is True
    manager.user_management.delete_user.assert_called_with("1")


@pytest.mark.asyncio
async def test_add_host_handles_xo_socket_error(mocker):
    # Patch the XOSocket's call method to raise the specific exception
    mocker.patch.object(
        XOSocket, "call", side_effect=XOSocketError("server already exists")
    )

    # Directly patch the `error` method of the logger used within the HostManagement
    with patch("logging.Logger.error") as mock_logger_error:
        manager = XOAManager("http://test")
        manager.host_management = HostManagement(XOAPI("http://test"))

        # Attempt to add host, which should trigger the patched XOSocketError
        await manager.add_host("localhost", "user", "pass")

        # Assert that the error method was called at least once
        mock_logger_error.assert_called()
