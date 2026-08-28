from dataclasses import dataclass
from typing import Any


@dataclass
class ToolMetadata:
    name: str
    description: str
    permission: str
    confirmation_level: str = "level_1"


class BaseTool:
    metadata: ToolMetadata

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
