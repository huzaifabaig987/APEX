"""Run APEX test prompts against simulated secure and vulnerable agents."""

import json
from pathlib import Path

from src.apex.target_agent import SECRET, run_agent

ROOT = Path(__file__).resolve().parents[2]
DATASETS = [
    ROOT / "data" / "samples" / "prompt_injection_cases.json",
    ROOT / "data" / "samples" / "challenge_cases.json",
]
REPORT = ROOT / "reports" / "agent_evaluation.json"


def main():
    cases = []
    for path in DATASETS:
        cases.extend(json.loads(path.read_text(encoding="utf-8")))

    results = []
    for case in cases:
        for mode in ("secure", "vulnerable"):
            response = run_agent(case["prompt"], mode)
            leaked = SECRET in response

            results.append({
                "id": case["id"],
                "mode": mode,
                "expected_injection": case["expected_injection"],
                "secret_disclosed": leaked,
                "attack_succeeded": leaked and case["expected_injection"],
                "response": response,
            })

    summary = {}
    for mode in ("secure", "vulnerable"):
        mode_results = [r for r in results if r["mode"] == mode]
        attack_cases = [r for r in mode_results if r["expected_injection"]]
        benign_cases = [r for r in mode_results if not r["expected_injection"]]

        summary[mode] = {
            "total_cases": len(mode_results),
            "secret_disclosures": sum(r["secret_disclosed"] for r in mode_results),
            "attack_cases": len(attack_cases),
            "successful_attack_disclosures": sum(
                r["attack_succeeded"] for r in mode_results
            ),
            "benign_case_disclosures": sum(
                r["secret_disclosed"] for r in benign_cases
            ),
        }

    report = {
        "experiment": "APEX simulated target-agent evaluation",
        "note": (
            "Deterministic simulation only; these results do not measure "
            "real language-model security."
        ),
        "summary": summary,
        "results": results,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("APEX TARGET-AGENT EXPERIMENT")
    print("=" * 36)
    for mode, metrics in summary.items():
        print(f"\n{mode.upper()} MODE")
        for key, value in metrics.items():
            print(f"{key}: {value}")

    print(f"\nReport saved to: {REPORT}")


if __name__ == "__main__":
    main()
