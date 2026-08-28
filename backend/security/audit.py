from dataclasses import dataclass, field
from typing import Any

from backend.utils.helpers import utc_now_iso


@dataclass
class AuditLogger:
    events: list[dict[str, Any]] = field(default_factory=list)

    def log(self, event_type: str, details: dict[str, Any]) -> None:
        self.events.append({
            "timestamp": utc_now_iso(),
            "type": event_type,
            "details": details,
        })

    def list_events(self) -> list[dict[str, Any]]:
        return list(self.events)

    def clear(self) -> None:
        self.events.clear()
