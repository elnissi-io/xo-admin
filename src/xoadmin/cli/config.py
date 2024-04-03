import json
import os
from typing import Optional

import click
import yaml
from pydantic import SecretStr

from xoadmin.cli.model import ENV_VARIABLE_MAPPING, XOAConfig
from xoadmin.cli.utils import (
    coro,
    load_xo_config,
    mask_sensitive,
    save_xo_config,
    update_config,
)


@click.group(name="config")
def config_commands():
    """Configuration management commands."""
    pass


@config_commands.command(name="info")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format.",
)
@click.option(
    "--sensitive", is_flag=True, default=False, help="Display sensitive information."
)
def config_info(format_, sensitive):
    """Display the current configuration."""
    config_model = load_xo_config()
    # Convert Pydantic model to dict, automatically handling SecretStr serialization
    config_dict = config_model.dict()
    # Optionally mask sensitive data
    config_dict = mask_sensitive(config_dict, show_sensitive=sensitive)

    formatted_output = (
        yaml.dump(config_dict, default_flow_style=False)
        if format_ == "yaml"
        else json.dumps(config_dict, indent=4)
    )
    click.echo(formatted_output)


@config_commands.command(name="set")
@click.argument("key")
@click.argument("value", required=False)  # Optional, for setting from env
@click.option(
    "--from-env", is_flag=True, help="Set the variable from an environment variable."
)
@click.option(
    "--env-var", help="Use a specific environment variable (overrides default)."
)
def config_set(key, value, from_env, env_var: Optional[str]):
    config_model = load_xo_config()

    if from_env:
        env_key = env_var if env_var else ENV_VARIABLE_MAPPING.get(key)
        if not env_key:
            click.echo(f"No environment variable mapping found for {key}.", err=True)
            return

        value = os.getenv(env_key)
        if value is None:
            click.echo(f"Environment variable {env_key} is not set.", err=True)
            return

    # Create a new config with the updated settings
    updated_config_model = update_config(config_model, key, value)

    # Save the updated model back to the config file
    save_xo_config(updated_config_model)
    click.echo(f"Updated configuration '{key}' with new value.")
