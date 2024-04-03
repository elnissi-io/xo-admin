import click

from xoadmin.api.host import HostManagement
from xoadmin.cli.utils import get_authenticated_api


@click.group(name="host")
def host_commands():
    """Manage hosts."""
    pass


@host_commands.command(name="add")
@click.argument("host")
@click.argument("username")
@click.argument("password")
@click.option(
    "--auto-connect",
    is_flag=True,
    default=True,
    help="Automatically connect to the host.",
)
@click.option(
    "--allow-unauthorized",
    is_flag=True,
    default=False,
    help="Allow unauthorized certificates.",
)
async def add_host(host, username, password, auto_connect, allow_unauthorized):
    """Add a new host."""
    api = await get_authenticated_api()
    host_management = HostManagement(api)
    await host_management.add_host(
        host, username, password, auto_connect, allow_unauthorized
    )
    click.echo(f"Added host {host}.")


# Add this to the cli group in main.py
