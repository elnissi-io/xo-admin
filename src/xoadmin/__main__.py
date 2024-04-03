import asyncio

import click

from xoadmin.configurator.configurator import XOAConfigurator


@click.group()
def cli():
    """XOA Admin CLI tool for managing Xen Orchestra instances."""
    pass


@cli.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to the configuration file.",
)
def configure(config):
    """Configure Xen Orchestra instances."""
    asyncio.run(run_configure(config))


async def run_configure(config):
    configurator = XOAConfigurator(config)
    await configurator.load_and_apply_configuration()


if __name__ == "__main__":
    cli()
