import asyncio

from xoadmin.manager import XOAManager


async def main():
    # Replace these with actual values
    XO_BASE_URL = "http://localhost:80"
    XO_USERNAME = "admin"
    XO_PASSWORD = "admin"
    HYPERVISOR_IP = "192.168.88.201"
    TERRAFORM_USER = "sa-terraform"
    TERRAFORM_PASSWORD = "1234"

    # Initialize the XO API client
    xoa_manager = XOAManager(XO_BASE_URL, verify_ssl=False)
    xoa_manager.authenticate(username=XO_USERNAME, password=XO_PASSWORD)

    # Create a new user
    await xoa_manager.create_user(
        email=TERRAFORM_USER, password=TERRAFORM_PASSWORD, permission="admin"
    )
    print(f"User {TERRAFORM_USER} created successfully.")

    # Add a new host
    host_details = {
        "host": HYPERVISOR_IP,
        "username": "root",  # Hypervisor's root username, change if necessary
        "password": "password",  # Hypervisor's root password, change if necessary
        "autoConnect": True,
    }
    await xoa_manager.add_host(host_details)
    print(f"Host {HYPERVISOR_IP} added successfully.")


if __name__ == "__main__":
    asyncio.run(main())
