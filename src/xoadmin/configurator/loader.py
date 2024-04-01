# src/xoa_container/configurator/config_loader.py
import yaml
from xoadmin.configurator.config import AppConfig

def load_config(config_path: str) -> AppConfig:
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    return AppConfig(**config_data)