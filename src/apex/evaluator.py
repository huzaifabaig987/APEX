import json
from pathlib import Path
from src.apex.baseline import detect_injection

def evaluate_file(dataset_path):
    path = Path(dataset_path)
    cases = json.loads(path.read_text(encoding="utf-8"))

    tp = tn = fp = fn = 0
    details = []

    for case in cases:
        expected = case["expected_injection"]
        predicted = detect_injection(case["prompt"])

        if expected and predicted:
            tp += 1
        elif not expected and not predicted:
            tn += 1
        elif not expected and predicted:
            fp += 1
        else:
            fn += 1

        details.append({
            "id": case["id"],
            "expected": expected,
            "predicted": predicted,
            "correct": expected == predicted,
        })

    total = len(cases)

    metrics = {
        "dataset": path.name,
        "total": total,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "accuracy": (tp + tn) / total if total else 0,
        "precision": tp / (tp + fp) if tp + fp else 0,
        "recall": tp / (tp + fn) if tp + fn else 0,
    }

    return metrics, details

if __name__ == "__main__":
    datasets = [
        "data/samples/prompt_injection_cases.json",
        "data/samples/challenge_cases.json",
    ]

    all_reports = []

    for dataset in datasets:
        metrics, details = evaluate_file(dataset)
        all_reports.append({"metrics": metrics, "details": details})

        print(f"\nDATASET: {metrics['dataset']}")
        print("-" * 40)

        for key, value in metrics.items():
            if key != "dataset":
                if isinstance(value, float):
                    print(f"{key}: {value:.3f}")
                else:
                    print(f"{key}: {value}")

        print("Errors:", [item["id"] for item in details if not item["correct"]])

    output = Path("reports/baseline_evaluation.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(all_reports, indent=2), encoding="utf-8")

    print(f"\nReport saved to {output}")
