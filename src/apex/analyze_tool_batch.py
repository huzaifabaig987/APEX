"""Analyze existing APEX tool-batch evaluation results."""

import json
from pathlib import Path

SOURCE = Path("reports/tool_batch_evaluation.json")
OUTPUT = Path("reports/tool_batch_analysis.json")


def rate(numerator, denominator):
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def analyze_mode(rows, mode):
    selected = [row for row in rows if row["mode"] == mode]
    attacks = [row for row in selected if row["label"] == "attack"]
    benign = [row for row in selected if row["label"] == "benign"]

    protected_requests = [
        row for row in selected
        if row["proposed_tool"] == "get_protected_record"
    ]
    blocked_requests = [
        row for row in protected_requests
        if not row["gateway_allowed"]
    ]

    return {
        "total_cases": len(selected),
        "attack_cases": len(attacks),
        "benign_cases": len(benign),
        "protected_tool_requests": len(protected_requests),
        "protected_tool_request_rate_pct": rate(
            len(protected_requests), len(selected)
        ),
        "attack_protected_tool_request_rate_pct": rate(
            sum(r["proposed_tool"] == "get_protected_record" for r in attacks),
            len(attacks),
        ),
        "benign_protected_tool_requests": sum(
            r["proposed_tool"] == "get_protected_record" for r in benign
        ),
        "benign_protected_tool_request_rate_pct": rate(
            sum(r["proposed_tool"] == "get_protected_record" for r in benign),
            len(benign),
        ),
        "protected_data_returns": sum(
            r["protected_data_returned"] for r in selected
        ),
        "access_block_rate_pct": rate(
            len(blocked_requests), len(protected_requests)
        ),
        "final_canary_disclosures": sum(
            r["canary_in_final_response"] for r in selected
        ),
        "final_disclosure_rate_pct": rate(
            sum(r["canary_in_final_response"] for r in selected),
            len(selected),
        ),
    }


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Evaluation report not found: {SOURCE}")

    report = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = report["results"]

    analysis = {
        "source_report": str(SOURCE),
        "model": report.get("model", "not recorded"),
        "method": (
            "Descriptive analysis of the existing batch report; "
            "no new model calls were made."
        ),
        "secure": analyze_mode(rows, "secure"),
        "vulnerable": analyze_mode(rows, "vulnerable"),
        "limitations": [
            "Only eight unique prompts were evaluated.",
            "Rates describe this dataset, not all possible attacks.",
            "Access-block rate uses protected-tool requests as its denominator.",
            "A returned protected record is not necessarily a final disclosure.",
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

    for mode in ("secure", "vulnerable"):
        print(f"\n{mode.upper()} MODE")
        for metric, value in analysis[mode].items():
            print(f"{metric}: {value}")

    print(f"\nAnalysis saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
