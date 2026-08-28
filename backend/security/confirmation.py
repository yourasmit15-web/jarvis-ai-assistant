from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from backend.utils.helpers import utc_now_iso


class ConfirmationLevel(str, Enum):
    SAFE = "level_1"
    SENSITIVE = "level_2"
    HIGH_RISK = "level_3"


@dataclass
class ConfirmationManager:
    pending: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def requires_confirmation(self, level: ConfirmationLevel) -> bool:
        return level in {ConfirmationLevel.SENSITIVE, ConfirmationLevel.HIGH_RISK}

    def request_confirmation(self, action: str, level: ConfirmationLevel, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        confirmation_id = str(uuid4())
        record = {
            "id": confirmation_id,
            "action": action,
            "level": level.value,
            "payload": payload or {},
            "status": "pending",
            "created_at": utc_now_iso(),
        }
        self.pending[confirmation_id] = record
        self.history.append(record.copy())
        return record

    def approve(self, confirmation_id: str) -> dict[str, Any] | None:
        record = self.pending.pop(confirmation_id, None)
        if not record:
            return None
        record = {**record, "status": "approved", "approved_at": utc_now_iso()}
        self.history.append(record)
        return record
