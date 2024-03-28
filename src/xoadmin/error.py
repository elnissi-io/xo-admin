class AuthenticationError(Exception):
    """Exception for authentication-related errors."""


class XOSocketError(Exception):
    """Exception raised for errors encountered within the Xo class."""


class ServerError(Exception):
    """Exception for server-related errors."""


class HostAlreadyExistsError(ServerError):
    """Exception when trying to add a host that already exists."""
