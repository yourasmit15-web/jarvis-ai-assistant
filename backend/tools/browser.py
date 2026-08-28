from backend.tools.base import BaseTool, ToolMetadata


class BrowserTool(BaseTool):
    metadata = ToolMetadata(
        name="browser",
        description="Browser automation stub for future phases",
        permission="computer.browser",
    )

    async def execute(self, **kwargs):
        return {"message": "Browser automation is a Phase 2 capability."}
