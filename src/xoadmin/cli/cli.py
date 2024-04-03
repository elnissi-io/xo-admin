import asyncio
from functools import update_wrapper

import click

from xoadmin.cli.apply import apply_config
from xoadmin.cli.config import config_commands
from xoadmin.cli.hosts import host_commands
from xoadmin.cli.storage import storage_commands
from xoadmin.cli.users import user_commands
from xoadmin.cli.vms import vm_commands


# Define the coro decorator
def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


# Custom Click command group with automatic coroutine wrapping
class AsyncClickGroup(click.Group):
    def command(self, *args, **kwargs):
        def decorator(f):
            return super().command(*args, **kwargs)(coro(f))

        return decorator


# Create the main CLI group using AsyncClickGroup
@click.group(cls=AsyncClickGroup)
def cli():
    """XOA Admin CLI tool for managing Xen Orchestra instances."""
    pass


cli.add_command(apply_config)
cli.add_command(user_commands)
cli.add_command(host_commands)
cli.add_command(vm_commands)
cli.add_command(storage_commands)
cli.add_command(config_commands)

if __name__ == "__main__":
    cli()
