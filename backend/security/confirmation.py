from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


class ConfirmationRequired(Exception):
    def __init__(self, request_id: str, level: int):
        self.request_id = request_id
        self.level = level
        super().__init__(f"Confirmation required: level {level}")


@dataclass
class ConfirmationRequest:
    id: str
    level: int
    tool: str
    summary: str
    approved: bool = False


@dataclass
class ConfirmationManager:
    requests: dict[str, ConfirmationRequest] = field(default_factory=dict)

    def get_confirmation_level(self, tool_name: str, payload: dict) -> int:
        if tool_name in {"search"}:
            return 1
        if tool_name in {"browser", "phone"}:
            return 2
        return 3

    def create_request(self, level: int, tool: str, summary: str) -> str:
        request_id = str(uuid4())
        self.requests[request_id] = ConfirmationRequest(id=request_id, level=level, tool=tool, summary=summary)
        return request_id

    def approve(self, request_id: str) -> bool:
        req = self.requests.get(request_id)
        if not req:
            return False
        req.approved = True
        return True

    def history(self) -> list[dict]:
        return [vars(r) for r in self.requests.values()]
