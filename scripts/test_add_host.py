import asyncio
import os

from xoadmin.api.manager import XOAManager


async def main():
    # Replace these with actual values
    XO_BASE_URL = "http://localhost:80"
    XO_USERNAME = "admin"
    XO_PASSWORD = "password"
    HYPERVISOR_IP = "192.168.88.201"
    TERRAFORM_USER = "sa-terraform"
    TERRAFORM_PASSWORD = "1234"

    # Initialize the XO API client
    xoa_manager = XOAManager(XO_BASE_URL, verify_ssl=False)
    await xoa_manager.authenticate(username=XO_USERNAME, password=XO_PASSWORD)

    # Create a new user
    await xoa_manager.create_user(
        email=TERRAFORM_USER, password=TERRAFORM_PASSWORD, permission="admin"
    )
    await xoa_manager.add_host(
        host=HYPERVISOR_IP,
        username="root",
        password=os.getenv("HYPERVISOR_ROOT_PASSWORD", ""),
        autoConnect=True,
        allowUnauthorized=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
