from dataclasses import dataclass, field


DEFAULT_PERMISSIONS = {
    "computer.screen": False,
    "computer.keyboard": False,
    "computer.mouse": False,
    "computer.files": False,
    "computer.applications": False,
    "computer.terminal": False,
    "phone.notifications": False,
    "phone.contacts": False,
    "phone.calendar": False,
    "phone.messages": False,
    "phone.calls": False,
    "phone.camera": False,
    "phone.location": False,
    "online_accounts.social_media": False,
    "online_accounts.email": False,
    "online_accounts.cloud_storage": False,
    "online_accounts.other_apis": False,
    "online.web_search": True,
}


@dataclass
class PermissionManager:
    permissions: dict[str, bool] = field(default_factory=lambda: DEFAULT_PERMISSIONS.copy())

    def list_permissions(self) -> dict[str, bool]:
        return dict(self.permissions)

    def check(self, permission: str) -> bool:
        return self.permissions.get(permission, False)

    def set_permission(self, permission: str, enabled: bool) -> None:
        self.permissions[permission] = bool(enabled)

    def revoke_all(self) -> None:
        for key in self.permissions:
            self.permissions[key] = False
