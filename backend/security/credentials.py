from dataclasses import dataclass, field


@dataclass
class CredentialStore:
    _store: dict[str, str] = field(default_factory=dict)

    def set(self, key: str, value: str) -> None:
        self._store[key] = value

    def get(self, key: str) -> str | None:
        return self._store.get(key)
