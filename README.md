# xoadmin

xoadmin is an asynchronous Python client for interacting with Xen Orchestra's REST API and WebSocket. It enables the management of VMs, users, storage, and more, through Xen Orchestra.

- Authenticate via WebSocket.
- Perform operations on VMs.
- Manage users, including creating and deleting users.
- Handle storage operations like listing storage repositories (SRs) and managing Virtual Disk Images (VDIs).

## Installation

To use the XO Admin Library, ensure you have Python 3.9+ installed.

1. **From Source:** Clone and install the package from source

```bash
git clone https://github.com/elnissi-io/xoadmin.git
pip install .
```

2. **From pip:** Simple pip install
```bash
pip install xoadmin
```

## Quick Start

1. Initialize the `XOAManager` with the base URL of your Xen Orchestra instance:

```python
from xoadmin.api.manager import XOAManager

manager = XOAManager(host="your-xo-instance-host", verify_ssl=False)
```

2. Authenticate using your Xen Orchestra credentials:

```python
await manager.authenticate(username="your-username", password="your-password")
```

3. Now, you can perform various operations through the manager:

```python
vms = await manager.list_all_vms()
print(vms)
```

Ensure you run your script in an environment that supports asynchronous execution, like:

```python
import asyncio

asyncio.run(main())
```

## Documentation

Currently a work in progress.

For more detailed information on available methods and their usage, refer to the source code in the `src/xoadmin` directory. Each module (`vm.py`, `user.py`, `storage.py`) contains classes with methods corresponding to the Xen Orchestra functionalities they manage.

## Command Line Interface (CLI)

```bash
Usage: xoadmin [OPTIONS] COMMAND [ARGS]...

  XOA Admin CLI tool for managing Xen Orchestra instances.

Options:
  --help  Show this message and exit.

Commands:
  apply    Apply configuration to Xen Orchestra instances.
  auth     Authentication management commands.
  config   Configuration management commands.
  host     Manage hosts.
  storage  Storage management commands.
  user     Manage users.
  vm       VM management commands.
```

The XO Admin Library provides a Command Line Interface (CLI) to simplify interaction with Xen Orchestra. Here's how you can use it:

1. **Installation:** Install either from source or using pip:

2. **Authentication:** Initialize the `XOAManager` with the base URL of your Xen Orchestra instance and authenticate using your credentials:

    In a container environment for instance:
    ```bash
    xoadmin config generate
    ```
    This will display a copyable config file you could manually create  in `~/.xoadmin/config`.

    Alternatively, you could tell it to write it to a file using `--output <filepath>`
    ```bash
    xoadmin config generate --output ~/.xoadmin/config
    ```

    `xoadmin config generate` will tell you which environment variables were not defined, you could then manually define the values needed under the config file
    ```terminal
    ➜ xoadmin git:(main) ✗ xoadmin config generate -o test.yml
    XOA configuration generated and saved to test.yml.
    # No environment variables were found.
    # Environment variables not defined (using defaults):
    # - XOA_HOST
    # - XOA_REST_API
    # - XOA_WEBSOCKET
    # - XOA_USERNAME
    # - XOA_PASSWORD
    # - XOA_VERIFY_SSL
    ```

3. **Performing Operations:** You can now perform various operations using the CLI.

    The cli utilizes a config file under ~/.xoadmin/config
    ```yaml
    xoa:
      host: localhost
      ws_url: ws://localhost
      rest_api: http://localhost:80
      verify_ssl: false
      password: admin
      username: admin@admin.net
    ```
    List vms
    ```
    xoadmin vm list
    ```
    List users
    ```
    xoadmin user list
    ```
    List hosts
    ```
    xoadmin host list
    ```
## Applying a Configuration

xoadmin allows you to quickly add hosts and users to an XOA instance using a YAML file:

1. Create a YAML file with your desired configuration settings. For example:

    ```yaml
    hypervisors:
      - host: 192.168.0.1
        username: root
        password: password
        allowUnauthorized: true

    users:
      - username: user
        password: password
        permission: admin
    ```

2. Apply the configuration using the `apply` command:

    ```
    xoadmin apply -f config.yaml
    ```

## Module Usage

You can also integrate the XO Admin Library directly into your Python scripts for more customized usage. Here's an example of how you can do this:

```python
import asyncio
from xoadmin.api.manager import XOAManager

async def main():
    # Initialize XOAManager
    manager = XOAManager(
        host="localhost",
        rest_api="http://localhost:80",
        websocket="ws://localhost",
        verify_ssl=False
    )
    
    # Authenticate
    await manager.authenticate(username="admin@admin.net", password="admin")

    # Perform operations
    vms = await manager.list_all_vms()
    print(vms)

    # Close session
    await manager.close()
```

```python
import asyncio
from xoadmin.api.api import XOAPI

async def main():
    api = XOAPI(
                rest_base_url="http://localhost:80", # without /rest
                ws_url="ws://localhost",
                verify_ssl=True,
            )

    await api.authenticate_with_websocket(
        "admin@admin.net",
        "admin",
    )
```

## Contributing and License

Contributions to the XO Admin Library are welcome! Please feel free to submit pull requests or open issues to discuss new features or improvements. This project is licensed under the Apache 2.0 License. For more details, refer to the [LICENSE](LICENSE) file.
