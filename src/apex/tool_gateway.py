"""Controlled gateway for APEX mock-tool access experiments."""

from src.apex.mock_secret_tool import get_public_status, get_protected_record


def request_tool(tool_name: str, mode: str = "secure") -> dict:
    """Dispatch a tool request under a selected test policy."""
    if mode not in ("secure", "vulnerable"):
        raise ValueError("Mode must be 'secure' or 'vulnerable'.")

    if tool_name == "get_public_status":
        return {
            "allowed": True,
            "tool": tool_name,
            "data": get_public_status(),
        }

    if tool_name == "get_protected_record":
        if mode == "secure":
            return {
                "allowed": False,
                "tool": tool_name,
                "error": "Access denied by secure gateway.",
            }

        return {
            "allowed": True,
            "tool": tool_name,
            "data": get_protected_record(),
        }

    return {
        "allowed": False,
        "tool": tool_name,
        "error": "Unknown tool.",
    }
