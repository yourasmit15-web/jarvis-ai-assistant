from __future__ import annotations

from dataclasses import dataclass, field


DEFAULT_PERMISSIONS = {
    "computer.screen": False,
    "computer.keyboard": False,
    "computer.mouse": False,
    "computer.files": False,
    "computer.applications": False,
    "computer.browser": False,
    "phone.notifications": False,
    "phone.contacts": False,
    "phone.calendar": False,
    "phone.messages": False,
    "phone.calls": False,
    "phone.camera": False,
    "phone.location": False,
    "online.social_media": False,
    "online.email": False,
    "online.cloud_storage": False,
    "online.search": True,
}


@dataclass
class PermissionManager:
    _permissions: dict[str, bool] = field(default_factory=lambda: DEFAULT_PERMISSIONS.copy())

    def list_permissions(self) -> dict[str, bool]:
        return dict(self._permissions)

    def check_permission(self, permission: str) -> bool:
        return bool(self._permissions.get(permission, False))

    def set_permission(self, permission: str, enabled: bool) -> None:
        self._permissions[permission] = enabled

    def bulk_set(self, updates: dict[str, bool]) -> dict[str, bool]:
        for key, enabled in updates.items():
            self.set_permission(key, enabled)
        return self.list_permissions()
