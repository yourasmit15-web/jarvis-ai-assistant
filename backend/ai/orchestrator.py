from __future__ import annotations

from dataclasses import dataclass

from backend.ai.brain import AIBrain
from backend.security.audit import AuditLogger
from backend.security.confirmation import ConfirmationManager, ConfirmationRequired
from backend.security.permissions import PermissionManager
from backend.tools.registry import ToolRegistry


@dataclass
class Orchestrator:
    brain: AIBrain
    tool_registry: ToolRegistry
    permissions: PermissionManager
    confirmations: ConfirmationManager
    audit: AuditLogger

    async def handle_chat(self, message: str) -> dict:
        intent = self.brain.classify_intent(message)
        tool = self.tool_registry.select_tool(intent)
        if not tool:
            response = self.brain.generate_response(message)
            self.brain.update_context(message, response)
            return {"response": response, "intent": intent, "used_tool": None}

        allowed = self.permissions.check_permission(tool.metadata.permission)
        self.audit.log("permission_check", {"permission": tool.metadata.permission, "allowed": allowed})
        if not allowed:
            return {"response": f"Permission '{tool.metadata.permission}' is disabled.", "intent": intent, "used_tool": None}

        level = self.confirmations.get_confirmation_level(tool.metadata.name, {"message": message})
        if level > 1:
            request_id = self.confirmations.create_request(level, tool.metadata.name, message)
            self.audit.log("confirmation_requested", {"request_id": request_id, "tool": tool.metadata.name})
            raise ConfirmationRequired(request_id=request_id, level=level)

        result = await self.tool_registry.execute(tool.metadata.name, query=message)
        self.audit.log("tool_used", {"tool": tool.metadata.name, "result": result})
        response = f"{self.brain.assistant_name}: {result.get('message', 'Done')}"
        self.brain.update_context(message, response)
        return {"response": response, "intent": intent, "used_tool": tool.metadata.name, "result": result}
