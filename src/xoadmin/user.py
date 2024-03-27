from xoadmin.api import XOAPI
from typing import Dict, List, Any

class UserManagement:
    """Manage user operations within Xen Orchestra."""
    
    def __init__(self, api: XOAPI) -> None:
        self.api = api

    def list_users(self) -> List[Dict[str, Any]]:
        """List all users."""
        return self.api.get('rest/v0/users')

    def create_user(self, email: str, password: str, permission: str = "none") -> Dict[str, Any]:
        """Create a new user with the specified details."""
        user_data = {"email": email, "password": password, "permission": permission}
        return self.api.post('rest/v0/users', json_data=user_data)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user by their ID."""
        return self.api.delete(f'rest/v0/users/{user_id}')
