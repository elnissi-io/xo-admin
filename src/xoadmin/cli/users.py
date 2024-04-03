import click

from xoadmin.api.user import UserManagement
from xoadmin.cli.utils import get_authenticated_api


@click.group(name="user")
def user_commands():
    """Manage users."""
    pass


@user_commands.command(name="list")
async def list_users():
    """List all users."""
    api = await get_authenticated_api()
    user_management = UserManagement(api)
    users = await user_management.list_users()
    for user in users:
        click.echo(f"User: {user['email']}")


@user_commands.command(name="create")
@click.argument("email")
@click.argument("password")
@click.option("--permission", default="none", help="User permission level.")
async def create_user(email, password, permission):
    """Create a new user."""
    api = await get_authenticated_api()
    user_management = UserManagement(api)
    await user_management.create_user(email, password, permission)
    click.echo(f"Created user {email} with permission {permission}.")


@user_commands.command(name="delete")
@click.argument("email")
async def delete_user(email):
    """Delete a user."""
    api = await get_authenticated_api()
    user_management = UserManagement(api)
    result = await user_management.delete_user(email)
    if result:
        click.echo(f"User {email} deleted successfully.")
    else:
        click.echo(f"Failed to delete user {email}.")
