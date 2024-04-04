# src/xoa_container/configurator/config_loader.py
import yaml

from xoadmin.configurator.config import ApplyConfig


def load_config(config_path: str) -> ApplyConfig:
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    if not config_data:
        raise ValueError(f"Empty ApplyConfig {config_path}")
    return ApplyConfig(**config_data)
