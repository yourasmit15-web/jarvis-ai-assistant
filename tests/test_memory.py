import pytest

from backend.ai.memory import MemoryStore


def test_memory_crud_and_secret_rejection(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.db"))
    memory_id = store.add_memory("preference", "Use dark mode")
    all_items = store.list_memory()
    assert any(item["id"] == memory_id for item in all_items)
    assert store.delete_memory(memory_id) is True

    with pytest.raises(ValueError):
        store.add_memory("secret", "my password is 123")
