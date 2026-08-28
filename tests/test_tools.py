from backend.tools.registry import ToolRegistry
from backend.tools.search import SearchTool


def test_tool_registry_executes_registered_tool():
    registry = ToolRegistry()
    registry.register(SearchTool())
    result = registry.execute("search", {"query": "jarvis"})
    assert result["status"] == "ok"
    assert result["results"]


def test_tool_registry_handles_unknown_tool():
    registry = ToolRegistry()
    result = registry.execute("missing", {})
    assert result["status"] == "error"
