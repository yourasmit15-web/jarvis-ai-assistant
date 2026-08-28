from backend.tools.base import BaseTool, ToolMetadata


class BrowserTool(BaseTool):
    metadata = ToolMetadata(
        name="browser",
        description="Browser automation stub",
        permission="computer.screen",
        confirmation_level="level_2",
    )

    def execute(self, payload: dict) -> dict:
        return {"status": "stub", "message": "Browser automation will be implemented in Phase 2", "payload": payload}
