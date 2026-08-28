from backend.tools.base import BaseTool


def tool_to_dict(tool: BaseTool) -> dict:
    return {
        "name": tool.metadata.name,
        "description": tool.metadata.description,
        "permission": tool.metadata.permission,
    }
