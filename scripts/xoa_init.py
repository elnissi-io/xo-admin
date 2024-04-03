# configure_xoa.py
import argparse
import asyncio
from xoadmin.configurator.configurator import XOAConfigurator

async def main(config_path):
    configurator = XOAConfigurator(config_path)
    await configurator.load_and_apply_configuration()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Configure Xen Orchestra instances.')
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to the configuration file.')
    args = parser.parse_args()
    
    asyncio.run(main(args.config))