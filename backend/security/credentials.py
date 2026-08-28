from dataclasses import dataclass
import os


@dataclass
class CredentialStore:
    """Phase 1 secure credential accessor via environment variables only."""

    def get(self, key: str) -> str | None:
        return os.getenv(key)
