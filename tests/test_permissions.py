from backend.security.permissions import PermissionManager


def test_permission_set_and_check():
    perms = PermissionManager()
    assert perms.check_permission("online.search") is True
    perms.set_permission("online.search", False)
    assert perms.check_permission("online.search") is False
