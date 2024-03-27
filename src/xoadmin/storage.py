
from xoadmin.api import XOAPI
from typing import Dict, List, Any

class StorageManagement:
    """Manage storage operations within Xen Orchestra."""
    
    def __init__(self, api: XOAPI) -> None:
        self.api = api

    def list_srs(self) -> List[Dict[str, Any]]:
        """List all Storage Repositories (SRs)."""
        return self.api.get('rest/v0/srs')

    def create_vdi(self, sr_id: str, size: int, name_label: str) -> Dict[str, Any]:
        """Create a new VDI on the specified SR."""
        vdi_data = {"size": size, "sr": sr_id, "name_label": name_label}
        return self.api.post('rest/v0/vdis', json_data=vdi_data)

    def delete_vdi(self, vdi_id: str) -> bool:
        """Delete a specified VDI."""
        return self.api.delete(f'rest/v0/vdis/{vdi_id}')
