import click

from xoadmin.api.vm import VMManagement
from xoadmin.cli.utils import coro, get_authenticated_api


@click.group(name="vm")
def vm_commands():
    """VM management commands."""
    pass


@vm_commands.command(name="list")
async def list_vms():
    """List all VMs."""
    api = await get_authenticated_api()
    vm_management = VMManagement(api)
    vms = await vm_management.list_vms()
    for vm in vms:
        click.echo(f"VM ID: {vm['id']}, Name: {vm['name_label']}")


@vm_commands.command(name="start")
@click.argument("vm_id")
async def start_vm(vm_id):
    """Start a VM."""
    api = await get_authenticated_api()
    vm_management = VMManagement(api)
    await vm_management.start_vm(vm_id)
    click.echo(f"VM {vm_id} started.")


@vm_commands.command(name="stop")
@click.argument("vm_id")
async def stop_vm(vm_id):
    """Stop a VM."""
    api = await get_authenticated_api()
    vm_management = VMManagement(api)
    await vm_management.stop_vm(vm_id)
    click.echo(f"VM {vm_id} stopped.")


@vm_commands.command(name="delete")
@click.argument("vm_id")
async def delete_vm(vm_id):
    """Delete a VM."""
    api = await get_authenticated_api()
    vm_management = VMManagement(api)
    await vm_management.delete_vm(vm_id)
    click.echo(f"VM {vm_id} deleted.")


# Assuming a create_from_template method exists and has the following parameters
@vm_commands.command(name="create-from-template")
@click.argument("template_id")
@click.argument("name")
@click.option("--description", default="", help="Description of the new VM.")
async def create_vm_from_template(template_id, name, description):
    """Create a new VM from a template."""
    api = await get_authenticated_api()
    vm_management = VMManagement(api)
    await vm_management.create_vm_from_template(template_id, name, description)
    click.echo(f"VM {name} created from template {template_id}.")
