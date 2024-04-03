from typing import Any, Dict, List

from xoadmin.api.api import XOAPI


class VMManagement:
    """Handles VM operations within Xen Orchestra."""

    def __init__(self, api: XOAPI) -> None:
        self.api = api

    async def list_vms(self) -> List[Dict[str, Any]]:
        """List all VMs."""
        return await self.api.get("rest/v0/vms")

    async def start_vm(self, vm_id: str) -> Dict[str, Any]:
        """Start a specified VM."""
        return await self.api.post(f"rest/v0/vms/{vm_id}/start", json_data={})

    async def stop_vm(self, vm_id: str) -> Dict[str, Any]:
        """Stop a specified VM."""
        return await self.api.post(f"rest/v0/vms/{vm_id}/stop", json_data={})

    async def delete_vm(self, vm_id: str) -> bool:
        """Delete a specified VM."""
        return await self.api.delete(f"rest/v0/vms/{vm_id}")

    async def create_vm_from_template(
        self, template_id: str, name: str, description: str = ""
    ) -> Dict[str, Any]:
        """Create a new VM from a specified template."""
        # This method would need to construct the appropriate payload
        # based on your Xen Orchestra's API requirements for VM creation
        vm_data = {
            "template": template_id,
            "name_label": name,
            "name_description": description,
        }
        return await self.api.post("rest/v0/vms", json_data=vm_data)

    async def list_template_vms(self) -> List[Dict[str, Any]]:
        """List all VM templates."""
        return await self.api.get("rest/v0/vm-templates")
