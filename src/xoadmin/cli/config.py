import json
import os
from typing import Optional

import click
import yaml

from xoadmin.cli.model import XOA, XOAConfig, XOASettings
from xoadmin.cli.options import output_format
from xoadmin.cli.utils import (
    load_xo_config,
    mask_sensitive,
    render,
    save_xo_config,
    update_config,
)


@click.group(name="config")
def config_commands():
    """Configuration management commands."""
    pass


@config_commands.command(name="info")
@click.option(
    "--sensitive", is_flag=True, default=False, help="Display sensitive information."
)
@output_format
def config_info(sensitive, format_):
    """Display the current configuration."""
    config_model = load_xo_config()
    # Convert Pydantic model to dict, automatically handling SecretStr serialization
    config_dict = config_model.dict()
    # Optionally mask sensitive data
    config_dict = mask_sensitive(config_dict, show_sensitive=sensitive)

    click.echo(render(config_dict, format_))


@config_commands.command(name="set")
@click.argument("key")
@click.argument("value", required=False)  # Optional, for setting from env
@click.option(
    "--from-env", is_flag=True, help="Set the variable from an environment variable."
)
@click.option(
    "--env-var", help="Use a specific environment variable (overrides default)."
)
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
def config_set(
    key, value, from_env, env_var: Optional[str], config_path: Optional[str] = None
):
    """Sets a value in the config file."""
    config_model = load_xo_config(config_path=config_path)
    if from_env:
        env_key = env_var if env_var else getattr(XOASettings, key)
        if not env_key:
            click.echo(f"No environment variable mapping found for {key}.", err=True)
            return

        value = os.getenv(env_key)
        if value is None:
            click.echo(f"Environment variable {env_key} is not set.", err=True)
            return
    try:
        key_path = XOASettings.__prefix__ + key
        updated_config_model = update_config(config_model, key_path, value)
        save_xo_config(config=updated_config_model, config_path=config_path)
        click.echo(f"Updated configuration '{key}' with new value.")
    except ValueError as e:
        # click.echo(f"{traceback.format_exc()}", err=True)
        click.echo(f"Error updating configuration: {e}", err=True)


@config_commands.command(name="generate")
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file path for the generated configuration.",
)
def generate_config(output):
    """
    Generate XOA configuration based on environment variables and save it to the specified output file.
    """
    # Collect configuration values from environment variables
    xoa_values = {}
    for key in dir(XOASettings):
        if not key.startswith("__") and key != "defaults":
            env_var = getattr(XOASettings, key)
            value = os.getenv(env_var)
            if value is not None:
                xoa_values[key] = value

    # Add defaults for missing fields
    for key, default_value in XOASettings.defaults.items():
        xoa_values.setdefault(key, default_value)

    # Create XOA model instance
    xoa = XOA(**xoa_values)

    # Create XOAConfig model instance
    xoa_config = XOAConfig(xoa=xoa)

    # Save the configuration to the specified output file
    if output:
        save_xo_config(config=xoa_config, config_path=output)
        click.echo(f"XOA configuration generated and saved to {output}.")
    else:
        click.echo("No output file specified. Configuration not saved.")
