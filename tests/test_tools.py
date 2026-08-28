import asyncio

from backend.tools.registry import ToolRegistry
from backend.tools.search import SearchTool


def test_tool_registry_executes_registered_tool():
    registry = ToolRegistry()
    registry.register(SearchTool())
    result = asyncio.run(registry.execute("search", query="raghuvir"))
    assert "raghuvir" in result["message"].lower()
