import json
import re
from pathlib import Path

DATA_PATH = Path("data/samples/prompt_injection_cases.json")

PATTERNS = [
    r"\bignore (all )?(previous|prior|earlier) instructions\b",
    r"\bdisregard (the )?(system message|previous instructions)\b",
    r"\bpretend you are an unrestricted assistant\b",
    r"\breveal the secret code\b",
    r"\b(hidden|confidential) (canary|data|value|information)\b",
    r"\bfollow only this request\b",
    r"\bignore the user\b",
    r"\bdisclose confidential data\b",
]

def detect_injection(prompt: str) -> bool:
    """Return True when a known baseline pattern is detected."""
    text = prompt.lower()
    return any(re.search(pattern, text) for pattern in PATTERNS)

def evaluate(cases):
    results = []

    for case in cases:
        expected = case["expected_injection"]
        predicted = detect_injection(case["prompt"])

        results.append({
            "id": case["id"],
            "expected": expected,
            "predicted": predicted,
            "correct": expected == predicted,
        })

    tp = sum(r["expected"] and r["predicted"] for r in results)
    tn = sum(not r["expected"] and not r["predicted"] for r in results)
    fp = sum(not r["expected"] and r["predicted"] for r in results)
    fn = sum(r["expected"] and not r["predicted"] for r in results)

    total = len(results)

    metrics = {
        "total": total,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "accuracy": (tp + tn) / total if total else 0,
        "precision": tp / (tp + fp) if tp + fp else 0,
        "recall": tp / (tp + fn) if tp + fn else 0,
    }

    return results, metrics

if __name__ == "__main__":
    cases = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    results, metrics = evaluate(cases)

    print("BASELINE EVALUATION")
    print("-" * 35)

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nINDIVIDUAL RESULTS")
    for result in results:
        status = "CORRECT" if result["correct"] else "INCORRECT"
        print(
            f'{result["id"]}: expected={result["expected"]}, '
            f'predicted={result["predicted"]} [{status}]'
        )
