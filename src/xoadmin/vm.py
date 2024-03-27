from xoadmin.api import XOAPI
from typing import Dict, List, Any

class VMManagement:
    """Handles VM operations within Xen Orchestra."""
    
    def __init__(self, api: XOAPI) -> None:
        self.api = api

    def list_vms(self) -> List[Dict[str, Any]]:
        """List all VMs."""
        return self.api.get('rest/v0/vms')

    def start_vm(self, vm_id: str) -> Dict[str, Any]:
        """Start a specified VM."""
        return self.api.post(f'rest/v0/vms/{vm_id}/start', json_data={})

    def stop_vm(self, vm_id: str) -> Dict[str, Any]:
        """Stop a specified VM."""
        return self.api.post(f'rest/v0/vms/{vm_id}/stop', json_data={})

    def delete_vm(self, vm_id: str) -> bool:
        """Delete a specified VM."""
        return self.api.delete(f'rest/v0/vms/{vm_id}')
