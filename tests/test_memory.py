import pytest

from backend.ai.memory import MemoryStore


def test_memory_add_list_delete(tmp_path):
    store = MemoryStore(str(tmp_path / "jarvis.db"))
    stored = store.add("preference", "Use concise responses")
    items = store.list()
    assert items[0]["id"] == stored["id"]
    assert store.delete(stored["id"]) is True


def test_memory_rejects_secrets(tmp_path):
    store = MemoryStore(str(tmp_path / "jarvis.db"))
    with pytest.raises(ValueError):
        store.add("security", "my password is 123")
