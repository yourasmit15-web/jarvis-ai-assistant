from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.ai.brain import AIBrain
from backend.ai.memory import MemoryStore
from backend.ai.orchestrator import Orchestrator
from backend.api.models import ChatRequest, ChatResponse, ConfirmRequest, MemoryRequest, PermissionsRequest
from backend.security.audit import AuditLogger
from backend.security.confirmation import ConfirmationManager, ConfirmationRequired
from backend.security.permissions import PermissionManager
from backend.tools.browser import BrowserTool
from backend.tools.computer import ComputerTool
from backend.tools.phone import PhoneTool
from backend.tools.registry import ToolRegistry
from backend.tools.search import SearchTool

router = APIRouter(prefix="/api")

brain = AIBrain()
memory = MemoryStore()
permissions = PermissionManager()
confirmations = ConfirmationManager()
audit = AuditLogger()
registry = ToolRegistry()
for tool in (SearchTool(), BrowserTool(), ComputerTool(), PhoneTool()):
    registry.register(tool)
orchestrator = Orchestrator(brain=brain, tool_registry=registry, permissions=permissions, confirmations=confirmations, audit=audit)
emergency_stopped = False


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    global emergency_stopped
    if emergency_stopped:
        raise HTTPException(status_code=423, detail="RAGHUVIR is stopped. Use /api/stop to resume.")
    try:
        result = await orchestrator.handle_chat(payload.message)
        return ChatResponse(**result)
    except ConfirmationRequired as exc:
        return ChatResponse(
            response=f"Action needs level {exc.level} confirmation.",
            intent="confirmation",
            used_tool=None,
            pending_confirmation_id=exc.request_id,
        )


@router.get("/chat/history")
def chat_history():
    return {"history": brain.history}


@router.post("/permissions")
def set_permissions(payload: PermissionsRequest):
    return {"permissions": permissions.bulk_set(payload.updates)}


@router.get("/permissions")
def get_permissions():
    return {"permissions": permissions.list_permissions()}


@router.post("/memory")
def add_memory(payload: MemoryRequest):
    memory_id = memory.add_memory(payload.category, payload.content)
    audit.log("memory_added", {"id": memory_id, "category": payload.category})
    return {"id": memory_id}


@router.get("/memory")
def get_memory(query: str | None = None):
    return {"items": memory.list_memory(query=query)}


@router.delete("/memory/{memory_id}")
def delete_memory(memory_id: int):
    if not memory.delete_memory(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")
    audit.log("memory_deleted", {"id": memory_id})
    return {"deleted": True}


@router.get("/activity-log")
def activity_log(event_type: str | None = None):
    return {"items": audit.list(event_type=event_type)}


@router.post("/confirm")
def approve_confirmation(payload: ConfirmRequest):
    approved = confirmations.approve(payload.request_id)
    if not approved:
        raise HTTPException(status_code=404, detail="Confirmation request not found")
    audit.log("confirmation_approved", {"request_id": payload.request_id})
    return {"approved": True}


@router.get("/status")
def status():
    return {
        "assistant": "RAGHUVIR",
        "status": "stopped" if emergency_stopped else "ready",
        "registered_tools": registry.list_tools(),
        "pending_confirmations": confirmations.history(),
    }


@router.post("/stop")
def stop(toggle: bool = True):
    global emergency_stopped
    emergency_stopped = bool(toggle)
    audit.log("emergency_stop", {"stopped": emergency_stopped})
    return {"stopped": emergency_stopped}
