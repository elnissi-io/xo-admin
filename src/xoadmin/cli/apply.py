import click

from xoadmin.cli.utils import get_authenticated_manager
from xoadmin.configurator.configurator import XOAConfigurator


@click.command(name="apply")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the configuration file.",
)
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
async def apply_config(file, config_path):
    """Apply configuration to Xen Orchestra instances."""
    xoa_manager = await get_authenticated_manager(config_path=config_path)
    configurator = XOAConfigurator(xoa_manager=xoa_manager)
    configurator.load(file)
    await configurator.apply()
    click.echo("Configuration applied successfully.")
