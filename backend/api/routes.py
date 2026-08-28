from collections import deque
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from backend.ai.brain import AIBrain
from backend.ai.memory import MemoryStore
from backend.ai.orchestrator import Orchestrator
from backend.api.models import (
    ChatRequest,
    ChatResponse,
    ConfirmationApproveRequest,
    MemoryRequest,
    MemoryUpdateRequest,
    PermissionUpdate,
)
from backend.security.audit import AuditLogger
from backend.security.confirmation import ConfirmationManager
from backend.security.permissions import PermissionManager
from backend.tools.browser import BrowserTool
from backend.tools.computer import ComputerTool
from backend.tools.phone import PhoneTool
from backend.tools.registry import ToolRegistry
from backend.tools.search import SearchTool

router = APIRouter(prefix="/api")

chat_history: deque[dict[str, str]] = deque(maxlen=200)
brain = AIBrain()
memory = MemoryStore("backend/jarvis.db")
permissions = PermissionManager()
confirmations = ConfirmationManager()
audit = AuditLogger()
tools = ToolRegistry()
for tool in (SearchTool(), BrowserTool(), ComputerTool(), PhoneTool()):
    tools.register(tool)
orchestrator = Orchestrator(
    brain=brain,
    memory=memory,
    tools=tools,
    permissions=permissions,
    confirmations=confirmations,
    audit=audit,
)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    result = orchestrator.process_message(payload.message)
    chat_history.append({"role": "user", "message": payload.message})
    chat_history.append({"role": "assistant", "message": result["response"]})
    return ChatResponse(**result)


@router.get("/chat/history")
def get_chat_history() -> list[dict[str, str]]:
    return list(chat_history)


@router.get("/permissions")
def list_permissions() -> dict[str, bool]:
    return permissions.list_permissions()


@router.post("/permissions")
def update_permission(payload: PermissionUpdate) -> dict[str, Any]:
    permissions.set_permission(payload.permission, payload.enabled)
    audit.log("permission_updated", {"permission": payload.permission, "enabled": payload.enabled})
    return {"status": "ok", "permissions": permissions.list_permissions()}


@router.get("/memory")
def list_memory(search: str | None = Query(default=None)) -> list[dict[str, Any]]:
    return memory.list(search=search)


@router.post("/memory")
def add_memory(payload: MemoryRequest) -> dict[str, Any]:
    try:
        stored = memory.add(payload.category, payload.content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    audit.log("memory_stored", {"id": stored["id"], "category": payload.category})
    return stored


@router.put("/memory/{memory_id}")
def update_memory(memory_id: int, payload: MemoryUpdateRequest) -> dict[str, Any]:
    try:
        updated = memory.update(memory_id, payload.content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail="Memory not found")
    audit.log("memory_updated", {"id": memory_id})
    return updated


@router.delete("/memory/{memory_id}")
def delete_memory(memory_id: int) -> dict[str, bool]:
    deleted = memory.delete(memory_id)
    if deleted:
        audit.log("memory_deleted", {"id": memory_id})
    return {"deleted": deleted}


@router.get("/activity-log")
def get_activity_log() -> list[dict[str, Any]]:
    return audit.list_events()


@router.post("/confirm")
def approve_confirmation(payload: ConfirmationApproveRequest) -> dict[str, Any]:
    approved = confirmations.approve(payload.confirmation_id)
    if not approved:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    audit.log("confirmation_approved", {"id": payload.confirmation_id})
    return approved


@router.get("/status")
def get_status() -> dict[str, Any]:
    return {
        "status": "running",
        "tools": tools.list_tools(),
        "pending_confirmations": list(confirmations.pending.values()),
    }


@router.post("/stop")
def emergency_stop() -> dict[str, str]:
    permissions.revoke_all()
    audit.log("emergency_stop", {"message": "All permissions revoked"})
    return {"status": "stopped", "message": "All permissions revoked"}
