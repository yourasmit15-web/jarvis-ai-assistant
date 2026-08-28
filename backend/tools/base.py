from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolMetadata:
    name: str
    description: str
    permission: str


class BaseTool(ABC):
    metadata: ToolMetadata

    @abstractmethod
    async def execute(self, **kwargs):
        raise NotImplementedError
