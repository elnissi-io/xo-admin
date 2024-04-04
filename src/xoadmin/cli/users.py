from typing import Optional

import click

from xoadmin.api.user import UserManagement
from xoadmin.cli.utils import get_authenticated_api


@click.group(name="user")
def user_commands():
    """Manage users."""
    pass


@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
@user_commands.command(name="list")
async def list_users(config_path: Optional[str] = None):
    """List all users."""
    api = await get_authenticated_api(config_path)
    user_management = UserManagement(api)
    users = await user_management.list_users()
    for user in users:
        click.echo(f"User: {user['email']}")


@user_commands.command(name="create")
@click.argument("email")
@click.argument("password")
@click.option("--permission", default="none", help="User permission level.")
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
async def create_user(email, password, permission, config_path: Optional[str] = None):
    """Create a new user."""
    api = await get_authenticated_api(config_path)
    user_management = UserManagement(api)
    await user_management.create_user(email, password, permission)
    click.echo(f"Created user {email} with permission {permission}.")


@user_commands.command(name="delete")
@click.argument("email")
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
async def delete_user(email, config_path: Optional[str] = None):
    """Delete a user."""
    api = await get_authenticated_api(config_path)
    user_management = UserManagement(api)
    result = await user_management.delete_user(email)
    if result:
        click.echo(f"User {email} deleted successfully.")
    else:
        click.echo(f"Failed to delete user {email}.")
