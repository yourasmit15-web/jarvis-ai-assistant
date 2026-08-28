from backend.security.permissions import PermissionManager


def test_permission_update_and_check():
    manager = PermissionManager()
    manager.set_permission("computer.screen", True)
    assert manager.check("computer.screen") is True
    manager.revoke_all()
    assert manager.check("computer.screen") is False
