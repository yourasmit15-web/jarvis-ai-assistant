from __future__ import annotations

from dataclasses import dataclass, field

from backend.tools.base import BaseTool


@dataclass
class ToolRegistry:
    _tools: dict[str, BaseTool] = field(default_factory=dict)

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.metadata.name] = tool

    def get_tool(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "permission": tool.metadata.permission,
            }
            for tool in self._tools.values()
        ]

    def select_tool(self, intent: str) -> BaseTool | None:
        mapping = {
            "search": "search",
        }
        name = mapping.get(intent)
        return self.get_tool(name) if name else None

    async def execute(self, name: str, **kwargs):
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' is not registered")
        return await tool.execute(**kwargs)
