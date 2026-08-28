from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuditLogger:
    entries: list[dict] = field(default_factory=list)

    def log(self, event_type: str, data: dict) -> None:
        self.entries.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": event_type,
                "data": data,
            }
        )

    def list(self, event_type: str | None = None) -> list[dict]:
        if not event_type:
            return list(self.entries)
        return [entry for entry in self.entries if entry["event_type"] == event_type]
