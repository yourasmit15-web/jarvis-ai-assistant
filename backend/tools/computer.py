from backend.tools.base import BaseTool, ToolMetadata


class ComputerTool(BaseTool):
    metadata = ToolMetadata(
        name="computer",
        description="Computer control stub for future phases",
        permission="computer.applications",
    )

    async def execute(self, **kwargs):
        return {"message": "Computer control is a future phase capability."}
