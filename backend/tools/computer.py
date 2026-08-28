from backend.tools.base import BaseTool, ToolMetadata


class ComputerTool(BaseTool):
    metadata = ToolMetadata(
        name="computer",
        description="Computer control stub",
        permission="computer.applications",
        confirmation_level="level_2",
    )

    def execute(self, payload: dict) -> dict:
        return {"status": "stub", "message": "Computer control will be implemented in Phase 2", "payload": payload}
