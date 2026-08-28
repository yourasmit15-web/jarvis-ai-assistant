from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    response: str
    intent: str
    subtasks: list[str]
    result: dict | None = None


class PermissionUpdate(BaseModel):
    permission: str
    enabled: bool


class MemoryRequest(BaseModel):
    category: str = Field(min_length=2, max_length=100)
    content: str = Field(min_length=1, max_length=5000)


class MemoryUpdateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class ConfirmationApproveRequest(BaseModel):
    confirmation_id: str
