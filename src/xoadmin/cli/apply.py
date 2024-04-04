import click

from xoadmin.configurator.configurator import XOAConfigurator


@click.command(name="apply")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the configuration file.",
)
@click.pass_context
async def apply_config(ctx, file):
    """Apply configuration to Xen Orchestra instances."""
    configurator = XOAConfigurator(file)
    await configurator.load_and_apply_configuration()
    click.echo("Configuration applied successfully.")
