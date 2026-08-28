from dataclasses import dataclass, field
from typing import Any

from backend.tools.base import BaseTool


@dataclass
class ToolRegistry:
    _tools: dict[str, BaseTool] = field(default_factory=dict)

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.metadata.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {
                "name": tool.metadata.name,
                "description": tool.metadata.description,
                "permission": tool.metadata.permission,
                "confirmation_level": tool.metadata.confirmation_level,
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        tool = self.get(name)
        if not tool:
            return {"status": "error", "message": f"Unknown tool: {name}"}
        return tool.execute(payload)
