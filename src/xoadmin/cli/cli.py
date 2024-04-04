import asyncio

import click

from xoadmin.cli.apply import apply_config
from xoadmin.cli.auth import auth_commands
from xoadmin.cli.config import config_commands
from xoadmin.cli.hosts import host_commands
from xoadmin.cli.storage import storage_commands
from xoadmin.cli.users import user_commands
from xoadmin.cli.vms import vm_commands


# Coroutine wrapper for command callbacks
def coro(f):
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(f):
            return asyncio.run(f(*args, **kwargs))
        else:
            return f(*args, **kwargs)

    return wrapper


# Recursively wrap command callbacks
def wrap_commands(commands):
    for command in commands:
        if isinstance(command, click.Group):
            wrap_commands(command.commands.values())
        elif command.callback is not None:
            command.callback = coro(command.callback)


# Create the main CLI group using click.Group
@click.group()
def cli():
    """XOA Admin CLI tool for managing Xen Orchestra instances."""
    pass


# Import and add your commands here
cli.add_command(apply_config)
cli.add_command(user_commands)
cli.add_command(host_commands)
cli.add_command(vm_commands)
cli.add_command(storage_commands)
cli.add_command(config_commands)
cli.add_command(auth_commands)

# Wrap command callbacks
wrap_commands(cli.commands.values())

# If executed directly, run the CLI
if __name__ == "__main__":
    cli()
