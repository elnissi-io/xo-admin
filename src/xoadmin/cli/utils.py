import asyncio
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Type, Union

import yaml
from pydantic import BaseModel, SecretStr, ValidationError, parse_obj_as

from xoadmin.api.api import XOAPI
from xoadmin.cli.model import XOAConfig

DEFAULT_CONFIG_PATH = os.path.join(Path.home(), ".xoadmin/config")


async def get_authenticated_api() -> XOAPI:
    """Get an authenticated XOAPI instance."""
    config = load_xo_config()
    api = XOAPI(rest_base_url=config.xoa.host, verify_ssl=False)
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


def convert_value(value: str, target_type: Union[type, str]):
    """Converts a string value to a specified target type."""
    type_mapping = {
        "boolean": lambda x: x.lower() in ("true", "1", "yes"),
        bool: lambda x: x.lower() in ("true", "1", "yes"),
        "integer": int,
        int: int,
        "number": float,
        float: float,
        "string": str,
        str: str,
        # Add more types or custom conversion functions as needed
    }

    conversion_function = type_mapping.get(target_type)
    if not conversion_function:
        raise ValueError(f"Unsupported target type for conversion: {target_type}")

    return conversion_function(value)


def get_field_type(model: BaseModel, field_name: str):
    """
    Get the Python type of a model field in Pydantic V2.
    """
    # Accessing the field from the model schema
    field_schema = model.schema()["properties"].get(field_name)

    if not field_schema:
        raise ValueError(f"Field '{field_name}' does not exist in the model schema.")

    # The field's type information is under 'type' in the schema. This is simplified,
    # complex types might require deeper inspection of the schema.
    field_type = field_schema.get("type")

    # This might need further refinement based on how complex your types are,
    # e.g., if you're using custom types or more complex structures like lists of models.

    return field_type


def mask_sensitive(data, show_sensitive=False):
    """Recursively mask sensitive data in the dictionary."""
    if isinstance(data, dict):
        return {k: mask_sensitive(v, show_sensitive) for k, v in data.items()}
    elif isinstance(data, SecretStr) and not show_sensitive:
        return "*********"
    elif isinstance(data, SecretStr) and show_sensitive:
        return data.get_secret_value()
    return data


def update_config(config_model: XOAConfig, key_path: str, value: str) -> BaseModel:
    """
    Updates the configuration model based on a dot-separated key path,
    automatically converting the value to the correct type based on the model's definition.
    """
    keys = key_path.split(".")
    if keys[0] == "xoa":  # Assuming all paths should start with 'xoa'
        keys = keys[1:]  # Remove the 'xoa' part to navigate within the XOA model

    current_model = config_model.xoa
    for key in keys[:-1]:
        # For nested models, this will navigate into the nested models
        current_model = getattr(current_model, key)

    final_key = keys[-1]
    field_type = get_field_type(current_model, final_key)
    converted_value = convert_value(value, field_type)

    # Set the converted value on the final field
    setattr(current_model, final_key, converted_value)
    return config_model


# Async wrapper for Click command to handle asyncio functions
def coro(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
