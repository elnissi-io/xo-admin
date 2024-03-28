# xoadmin

xoadmin is an asynchronous Python client for interacting with Xen Orchestra's REST API and WebSocket. It enables the management of VMs, users, storage, and more, through Xen Orchestra.

- Authenticate via WebSocket.
- Perform operations on VMs.
- Manage users, including creating and deleting users.
- Handle storage operations like listing storage repositories (SRs) and managing Virtual Disk Images (VDIs).

## Installation

To use the XO Admin Library, ensure you have Python 3.7+ installed. This library depends on `httpx` and `websockets` for asynchronous HTTP and WebSocket communication, respectively.

1. Clone this repository.
2. Install the package

```sh
pip install .
```

## Quick Start

1. Initialize the `XOAManager` with the base URL of your Xen Orchestra instance:

```python
from xoadmin.manager import XOAManager

manager = XOAManager("http://your-xo-instance.com", verify_ssl=False)
```

2. Authenticate using your Xen Orchestra credentials:

```python
await manager.authenticate(username="your-username", password="your-password")
```

3. Now, you can perform various operations, such as listing all VMs:

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

For more detailed information on available methods and their usage, refer to the source code in the `src/xoadmin` directory. Each module (`vm.py`, `user.py`, `storage.py`) contains classes with methods corresponding to the Xen Orchestra functionalities they manage.

## Contributing

Contributions to the XO Admin Library are welcome! Please feel free to submit pull requests or open issues to discuss new features or improvements.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
