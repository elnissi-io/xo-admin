import click

from xoadmin.api.storage import StorageManagement
from xoadmin.cli.options import output_format
from xoadmin.cli.utils import get_authenticated_api, render


@click.group(name="storage")
def storage_commands():
    """Storage management commands."""
    pass


@storage_commands.command(name="list")
@output_format
@click.option("--raw", is_flag=True, default=False, help="Display full details of SRs.")
async def list_srs(format_: str, raw: bool):
    """List all Storage Repositories (SRs)."""
    api = await get_authenticated_api()
    storage_management = StorageManagement(api)
    srs = await storage_management.list_srs()

    if raw:
        click.echo(render(srs, format_))
    else:
        filtered_srs = []
        for sr in srs:
            filtered_srs.append(
                {
                    "id": sr.get("id", ""),
                    "name_label": sr.get("name_label", ""),
                    "uuid": sr.get("uuid", ""),
                    "type": sr.get("SR_type", ""),
                }
            )
        click.echo(render(filtered_srs, format_))


@storage_commands.command(name="create-vdi")
@click.argument("sr_id")
@click.argument("size", type=int)
@click.argument("name_label")
async def create_vdi(sr_id, size, name_label):
    """Create a new VDI on the specified SR."""
    api = await get_authenticated_api()
    storage_management = StorageManagement(api)
    vdi = await storage_management.create_vdi(sr_id, size, name_label)
    click.echo(f"VDI {vdi['id']} created in SR {sr_id}.")


@storage_commands.command(name="delete-vdi")
@click.argument("vdi_id")
async def delete_vdi(vdi_id):
    """Delete a specified VDI."""
    api = await get_authenticated_api()
    storage_management = StorageManagement(api)
    await storage_management.delete_vdi(vdi_id)
    click.echo(f"VDI {vdi_id} deleted.")


# Make sure to add the storage_commands group to your main cli group in main.py
