from dataclasses import dataclass

from backend.ai.brain import AIBrain
from backend.ai.memory import MemoryStore
from backend.security.audit import AuditLogger
from backend.security.confirmation import ConfirmationLevel, ConfirmationManager
from backend.security.permissions import PermissionManager
from backend.tools.registry import ToolRegistry


@dataclass
class Orchestrator:
    brain: AIBrain
    memory: MemoryStore
    tools: ToolRegistry
    permissions: PermissionManager
    confirmations: ConfirmationManager
    audit: AuditLogger

    def _intent_to_tool(self, intent: str) -> str | None:
        return {
            "web_search": "search",
            "computer_action": "computer",
            "phone_action": "phone",
        }.get(intent)

    def process_message(self, message: str) -> dict:
        intent = self.brain.classify_intent(message)
        subtasks = self.brain.decompose_task(message)
        self.audit.log("intent_classified", {"intent": intent.intent, "confidence": intent.confidence})

        if intent.intent == "store_memory":
            stored = self.memory.add("user_preference", intent.entities.get("content", message))
            self.audit.log("memory_stored", {"id": stored["id"]})
            return {"response": "Stored that preference in memory.", "intent": intent.intent, "subtasks": subtasks, "result": stored}

        tool_name = self._intent_to_tool(intent.intent)
        if not tool_name:
            return {"response": self.brain.generate_response(intent), "intent": intent.intent, "subtasks": subtasks, "result": None}

        tool = self.tools.get(tool_name)
        if not tool:
            return {"response": f"No tool found for {intent.intent}", "intent": intent.intent, "subtasks": subtasks, "result": None}

        permission_name = tool.metadata.permission
        has_permission = self.permissions.check(permission_name)
        self.audit.log("permission_checked", {"permission": permission_name, "allowed": has_permission})
        if not has_permission:
            return {
                "response": f"Permission '{permission_name}' is disabled. Enable it in Permission Manager.",
                "intent": intent.intent,
                "subtasks": subtasks,
                "result": None,
            }

        level = ConfirmationLevel(tool.metadata.confirmation_level)
        if self.confirmations.requires_confirmation(level):
            pending = self.confirmations.request_confirmation(
                action=f"tool:{tool_name}",
                level=level,
                payload=intent.entities,
            )
            self.audit.log("confirmation_requested", {"id": pending["id"], "tool": tool_name})
            return {
                "response": f"Confirmation required for {tool_name} ({level.value}).",
                "intent": intent.intent,
                "subtasks": subtasks,
                "result": {"confirmation": pending},
            }

        result = self.tools.execute(tool_name, intent.entities)
        self.audit.log("tool_executed", {"tool": tool_name, "status": result.get("status")})
        response = self.brain.generate_response(intent, result)
        return {"response": response, "intent": intent.intent, "subtasks": subtasks, "result": result}
