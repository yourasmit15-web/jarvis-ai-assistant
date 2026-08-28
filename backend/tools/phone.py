from backend.tools.base import BaseTool, ToolMetadata


class PhoneTool(BaseTool):
    metadata = ToolMetadata(
        name="phone",
        description="Phone control stub for future phases",
        permission="phone.notifications",
    )

    async def execute(self, **kwargs):
        return {"message": "Phone control is a future phase capability."}
