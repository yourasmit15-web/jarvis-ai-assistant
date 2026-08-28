from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AIBrain:
    assistant_name: str = "RAGHUVIR"
    history: list[dict[str, str]] = field(default_factory=list)

    def classify_intent(self, message: str) -> str:
        text = message.lower()
        if any(word in text for word in ["search", "find", "look up"]):
            return "search"
        if any(word in text for word in ["permission", "allow", "revoke"]):
            return "permissions"
        if any(word in text for word in ["remember", "memory", "store"]):
            return "memory"
        if any(word in text for word in ["stop", "halt", "emergency"]):
            return "stop"
        return "general"

    def decompose_task(self, message: str) -> list[str]:
        parts = [p.strip() for p in message.replace(" then ", " and ").split(" and ")]
        return [p for p in parts if p]

    def update_context(self, user_message: str, assistant_response: str) -> None:
        self.history.append({"user": user_message, "assistant": assistant_response})
        self.history = self.history[-50:]

    def generate_response(self, message: str, context: dict[str, Any] | None = None) -> str:
        intent = self.classify_intent(message)
        if intent == "general" and not context:
            return f"I'm {self.assistant_name}, your personal AI assistant. How can I help?"
        return f"{self.assistant_name} understood intent '{intent}' and is ready to continue."
