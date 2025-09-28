#!/usr/bin/env python3
import sys
import json
import time
import metrics


def parse_input(path):
    with open(path, "r", encoding="utf-8") as f:
        line = f.read().strip()
    parts = [p.strip() for p in line.split(",")]
    while len(parts) < 3:
        parts.append("")
    return {
        "code_url": parts[0],
        "dataset_url": parts[1],
        "model_url": parts[2],
    }


def print_ndjson(obj):
    print(json.dumps(obj, ensure_ascii=False))


def main(argv):
    if len(argv) != 2:
        print("Usage: python runner.py <input_file>", file=sys.stderr)
        sys.exit(2)

    inputs = parse_input(argv[1])

    start = time.time()
    results = metrics.run_all(inputs)
    total_latency = time.time() - start

    threshold = 2.0
    print_ndjson(
        {
            "metric": "latency_ok",
            "score": 1 if total_latency < threshold else 0,
            "details": {"latency_s": round(total_latency, 4), "threshold_s": threshold},
        }
    )

    for r in results or []:
        score = 1 if r.get("score") == 1 else 0
        print_ndjson(
            {
                "metric": r.get("metric"),
                "score": score,
                "details": r.get("details", {}),
            }
        )


if __name__ == "__main__":
    main(sys.argv)
