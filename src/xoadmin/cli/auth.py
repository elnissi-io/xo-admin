import os
from typing import Optional

import click

from xoadmin.cli.model import ENV_VARIABLE_MAPPING
from xoadmin.cli.utils import get_authenticated_manager, load_xo_config


@click.group(name="auth")
def auth_commands():
    """Authentication management commands."""
    pass


@auth_commands.command(name="test")
@click.argument("username", default=None, required=False)
@click.argument("password", default=None, required=False)
@click.option(
    "--from-env",
    is_flag=True,
    help="Set the username and password from environment variables.",
)
@click.option(
    "--env-var-username",
    help="Use a specific environment variable for the username.",
)
@click.option(
    "--env-var-password",
    help="Use a specific environment variable for the password.",
)
@click.option(
    "-c", "--config-path", default=None, help="Use a specific configuration file."
)
async def auth_test(
    username,
    password,
    from_env,
    env_var_username: Optional[str],
    env_var_password: Optional[str],
    config_path: Optional[str] = None,
):
    config_model = load_xo_config(config_path=config_path)
    if from_env:
        env_username = (
            env_var_username
            if env_var_username
            else ENV_VARIABLE_MAPPING.get("username")
        )
        env_password = (
            env_var_password
            if env_var_password
            else ENV_VARIABLE_MAPPING.get("password")
        )
        if not env_username or not env_password:
            click.echo(
                "Environment variable mappings for username and password are incomplete.",
                err=True,
            )
            return

        username = os.getenv(env_username)
        password = os.getenv(env_password)
        if username is None or password is None:
            click.echo(
                "Environment variables for username and/or password are not set.",
                err=True,
            )
            return
    try:
        manager = await get_authenticated_manager(
            config_path=config_path, username=username, password=password
        )
        click.echo("Authentication test successful.")
    except Exception as e:
        click.echo(f"Error during authentication test: {e}", err=True)
