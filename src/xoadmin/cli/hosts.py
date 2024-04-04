import click

from xoadmin.api.host import HostManagement
from xoadmin.cli.options import output_format
from xoadmin.cli.utils import get_authenticated_api, render


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


@host_commands.command(name="list")
@output_format
async def list_hosts(format_: str):
    """List all registered hosts."""
    api = await get_authenticated_api()
    host_management = HostManagement(api)
    hosts = await host_management.list_hosts()
    if hosts:
        click.echo(render(hosts, format_))  # Example: using 'name' key
    else:
        click.echo("No hosts found.")


@host_commands.command(name="delete")
@click.argument("host_id")
async def delete_host(host_id):
    """Delete a host by ID."""
    confirmation = click.confirm(f"Are you sure you want to delete host {host_id}?")
    if confirmation:
        api = await get_authenticated_api()
        host_management = HostManagement(api)
        result = await host_management.delete_host(host_id)

        if result.get("result"):
            click.echo(render(result, "yaml"))
            click.echo(f"Host {host_id} deleted.")
        else:
            click.echo(f"Failed to delete host {host_id}. Host might not exist.")

    else:
        click.echo("Deletion canceled.")
