"""Run a safe, synthetic APEX tool-gateway comparison."""

import json
from pathlib import Path
from src.apex.tool_gateway import request_tool

REPORT = Path("reports/tool_gateway_test.json")


def main():
    results = []

    for mode in ("secure", "vulnerable"):
        for tool_name in ("get_public_status", "get_protected_record"):
            result = request_tool(tool_name, mode)
            data = result.get("data", {})

            # Never print or store the actual canary in this report.
            results.append({
                "mode": mode,
                "tool": tool_name,
                "allowed": result["allowed"],
                "error": result.get("error"),
                "canary_present_in_tool_result": "canary" in data,
            })

            print(
                f"Mode: {mode} | Tool: {tool_name} | "
                f"Allowed: {result['allowed']} | "
                f"Canary returned: {'canary' in data}"
            )

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"\nGateway test passed: {len(results)} requests evaluated.")
    print(f"Report saved to: {REPORT}")


if __name__ == "__main__":
    main()
