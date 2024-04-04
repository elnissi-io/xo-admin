from typing import Optional

from xoadmin.api.manager import XOAManager
from xoadmin.configurator.config import AppConfig
from xoadmin.configurator.loader import load_config


class XOAConfigurator:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.app_config: Optional[AppConfig] = None

    async def load_and_apply_configuration(self):
        self.app_config = load_config(self.config_path)

        # Initialize XOAManager with XOA instance details
        xoa_manager = XOAManager(
            self.app_config.xoa.host,
            self.app_config.xoa.rest_api,
            self.app_config.xoa.websocket,
            verify_ssl=False,
        )
        await xoa_manager.authenticate(
            username=self.app_config.xoa.username, password=self.app_config.xoa.password
        )
        # Create users
        for user in self.app_config.users:
            await xoa_manager.create_user(
                email=user.username, password=user.password, permission=user.permission
            )

        # Add hypervisors
        for hypervisor in self.app_config.hypervisors:
            await xoa_manager.add_host(
                host=hypervisor.host,
                username=hypervisor.username,
                password=hypervisor.password,
                autoConnect=hypervisor.autoConnect,
                allowUnauthorized=hypervisor.allowUnauthorized,
            )

        await xoa_manager.close()
