from backend.tools.base import BaseTool, ToolMetadata


class PhoneTool(BaseTool):
    metadata = ToolMetadata(
        name="phone",
        description="Phone control stub",
        permission="phone.notifications",
        confirmation_level="level_2",
    )

    def execute(self, payload: dict) -> dict:
        return {"status": "stub", "message": "Phone control will be implemented in Phase 3", "payload": payload}
