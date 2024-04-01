import asyncio
import click
from xoadmin.configurator.configurator import XOAConfigurator

# Async wrapper for Click command to handle asyncio functions
def coro(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group()
def cli():
    """XOA Admin CLI tool for managing Xen Orchestra instances."""
    pass

@coro
@cli.command()
@click.option('-c', '--config', type=click.Path(exists=True), required=True, help='Path to the configuration file.')
async def configure(config):
    """Configure Xen Orchestra instances."""
    configurator = XOAConfigurator(config)
    await configurator.load_and_apply_configuration()

if __name__ == "__main__":
    cli()
