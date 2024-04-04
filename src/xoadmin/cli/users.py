from typing import Optional

import click

from xoadmin.api.user import UserManagement
from xoadmin.cli.options import output_format
from xoadmin.cli.utils import get_authenticated_api, render


@click.group(name="user")
def user_commands():
    """Manage users."""
    pass


@user_commands.command(name="list")
@output_format
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
async def list_users(format_: str, config_path: Optional[str] = None):
    """List all users with an option for raw information."""
    api = await get_authenticated_api(config_path)
    user_management = UserManagement(api)
    user_paths = await user_management.list_users()

    users = []
    for path in user_paths:
        user_details = await user_management.get_user_details(path)
        users.append(user_details)
    click.echo(render(users, format_))


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
