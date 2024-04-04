from typing import Any, Dict, List

from xoadmin.api.api import XOAPI


class StorageManagement:
    """Manage storage operations within Xen Orchestra."""

    def __init__(self, api: XOAPI) -> None:
        self.api = api

    async def list_srs(self) -> List[Dict[str, Any]]:
        """List all Storage Repositories (SRs) with basic information."""
        srs = await self.api.get("rest/v0/srs")

        # Extract SR IDs from the URLs
        sr_ids = [sr.split("/")[-1] for sr in srs]

        # Fetch detailed information for each storage repository
        detailed_srs = []
        for sr_id in sr_ids:
            detailed_sr = await self.get_sr_details(sr_id)
            detailed_srs.append(detailed_sr)

        return detailed_srs

    async def get_sr_details(self, sr_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific Storage Repository (SR)."""
        return await self.api.get(f"rest/v0/srs/{sr_id}?expand=all")

    async def create_vdi(
        self, sr_id: str, size: int, name_label: str
    ) -> Dict[str, Any]:
        """Create a new VDI on the specified SR."""
        vdi_data = {"size": size, "sr": sr_id, "name_label": name_label}
        return await self.api.post("rest/v0/vdis", json_data=vdi_data)

    async def delete_vdi(self, vdi_id: str) -> bool:
        """Delete a specified VDI."""
        return await self.api.delete(f"rest/v0/vdis/{vdi_id}")
