from dataclasses import dataclass

from backend.tools.utils import normalize_text


@dataclass
class IntentResult:
    intent: str
    confidence: float
    entities: dict[str, str]


class AIBrain:
    """Phase 1 lightweight NLU with rule-based intent classification."""

    def classify_intent(self, message: str) -> IntentResult:
        text = normalize_text(message)

        if any(word in text for word in ["search", "find", "look up"]):
            return IntentResult(intent="web_search", confidence=0.85, entities={"query": message})
        if any(word in text for word in ["open", "launch", "click"]):
            return IntentResult(intent="computer_action", confidence=0.7, entities={"command": message})
        if any(word in text for word in ["message", "call", "phone"]):
            return IntentResult(intent="phone_action", confidence=0.7, entities={"command": message})
        if any(word in text for word in ["remember", "save preference"]):
            return IntentResult(intent="store_memory", confidence=0.8, entities={"content": message})

        return IntentResult(intent="chat", confidence=0.6, entities={})

    def decompose_task(self, message: str) -> list[str]:
        return [segment.strip() for segment in message.split(" and ") if segment.strip()]

    def generate_response(self, intent: IntentResult, outcome: dict | None = None) -> str:
        if intent.intent == "chat":
            return "I understood your message. Tell me what task you want me to run."
        if not outcome:
            return f"Intent identified as {intent.intent}."
        if outcome.get("status") in {"ok", "stub"}:
            return f"Completed {intent.intent}: {outcome.get('message', 'done')}"
        return f"I could not complete {intent.intent}: {outcome.get('message', 'unknown error')}"
