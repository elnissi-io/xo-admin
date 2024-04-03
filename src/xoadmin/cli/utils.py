import asyncio
import os
from copy import deepcopy
from pathlib import Path

import yaml
from pydantic import SecretStr

from xoadmin.api.api import XOAPI
from xoadmin.cli.model import XOAConfig

DEFAULT_CONFIG_PATH = os.path.join(Path.home(), ".xoadmin/config")


async def get_authenticated_api() -> XOAPI:
    """Get an authenticated XOAPI instance."""
    config = load_xo_config()
    api = XOAPI(config.xoa.rest_base_url, verify_ssl=False)
    await api.authenticate_with_websocket(config.xoa.username, config.xoa.password)
    return api


def load_xo_config(config_path=DEFAULT_CONFIG_PATH) -> XOAConfig:
    """Load XO configuration using Pydantic, handling nested structure."""
    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        # Pydantic directly supports nested structures
        return XOAConfig(**config_data)
    except Exception as e:
        raise FileNotFoundError(f"Could not load config file from {config_path}: {e}")


def save_xo_config(config: XOAConfig, config_path=DEFAULT_CONFIG_PATH):
    """Save XO configuration using Pydantic, ensuring SecretStr fields are serialized correctly."""
    config_data = config.dict(by_alias=True, exclude_unset=True)

    # Manually process SecretStr to ensure it's saved as plain string
    def serialize_secretstr(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = serialize_secretstr(v)
        elif isinstance(obj, SecretStr):
            return obj.get_secret_value()  # Convert SecretStr to plain string
        return obj

    config_data = serialize_secretstr(config_data)

    with open(config_path, "w") as f:
        yaml.dump(config_data, f)


def mask_sensitive(data, show_sensitive=False):
    """Recursively mask sensitive data in the dictionary."""
    if isinstance(data, dict):
        return {k: mask_sensitive(v, show_sensitive) for k, v in data.items()}
    elif isinstance(data, SecretStr) and not show_sensitive:
        return "*********"
    elif isinstance(data, SecretStr) and show_sensitive:
        return data.get_secret_value()
    return data


def update_config(config_model, key, value):
    """Update the configuration model with the new value."""
    updated_config_model = deepcopy(config_model)

    # Use dot notation access for Pydantic models
    try:
        field_path = key.split(".")
        # Navigate through the nested model to the final field
        nested_model = updated_config_model.xoa
        for part in field_path[:-1]:
            nested_model = getattr(nested_model, part)
        final_key = field_path[-1]

        # Check if we are updating a SecretStr field
        if isinstance(getattr(nested_model, final_key), SecretStr):
            setattr(nested_model, final_key, SecretStr(value))
        else:
            setattr(nested_model, final_key, value)
    except AttributeError as e:
        raise AttributeError(f"Could not find field '{key}' in config model: {e}")
        return config_model

    return updated_config_model


# Async wrapper for Click command to handle asyncio functions
def coro(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
