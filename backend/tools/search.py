from backend.tools.base import BaseTool, ToolMetadata


class SearchTool(BaseTool):
    metadata = ToolMetadata(
        name="search",
        description="Search public web information",
        permission="online.search",
    )

    async def execute(self, **kwargs):
        query = kwargs.get("query", "")
        return {"message": f"Search prepared for: {query}", "results": []}
