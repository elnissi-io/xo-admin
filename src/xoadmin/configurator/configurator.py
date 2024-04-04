from typing import Optional

from xoadmin.api.manager import XOAManager
from xoadmin.configurator.config import ApplyConfig
from xoadmin.configurator.loader import load_config


class XOAConfigurator:
    def __init__(
        self, apply_config: ApplyConfig = None, xoa_manager: XOAManager = None
    ):
        self.apply_config: ApplyConfig = apply_config
        self.xoa_manager: Optional[XOAManager] = xoa_manager

    def load(self, config_path: str):
        self.apply_config = load_config(config_path)

    async def apply(
        self, apply_config: ApplyConfig = None, xoa_manager: XOAManager = None
    ):
        if not xoa_manager:
            xoa_manager = self.xoa_manager
        if not xoa_manager:
            raise ValueError("No XOAPI instance provided.")
        if not apply_config:
            apply_config = self.apply_config
        if not apply_config:
            raise ValueError("No ApplyConfig provided.")
        # Create users
        for user in self.apply_config.users:
            await xoa_manager.create_user(
                email=user.username, password=user.password, permission=user.permission
            )

        # Add hypervisors
        for hypervisor in self.apply_config.hypervisors:
            await xoa_manager.add_host(
                host=hypervisor.host,
                username=hypervisor.username,
                password=hypervisor.password,
                autoConnect=hypervisor.autoConnect,
                allowUnauthorized=hypervisor.allowUnauthorized,
            )

        await xoa_manager.close()
