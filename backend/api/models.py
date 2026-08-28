from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    response: str
    intent: str
    used_tool: str | None = None
    pending_confirmation_id: str | None = None


class PermissionsRequest(BaseModel):
    updates: dict[str, bool]


class MemoryRequest(BaseModel):
    category: str
    content: str


class ConfirmRequest(BaseModel):
    request_id: str
