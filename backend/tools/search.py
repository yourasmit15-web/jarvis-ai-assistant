from backend.tools.base import BaseTool, ToolMetadata


class SearchTool(BaseTool):
    metadata = ToolMetadata(
        name="search",
        description="Search the web for public information",
        permission="online.web_search",
        confirmation_level="level_1",
    )

    def execute(self, payload: dict[str, str]) -> dict[str, str | list[str]]:
        query = payload.get("query", "").strip()
        if not query:
            return {"status": "error", "message": "query is required"}
        return {
            "status": "ok",
            "query": query,
            "results": [f"Stub result for: {query}"],
        }
