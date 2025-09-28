#!/usr/bin/env python3
import sys
import json
from metrics import run
from typing import Dict, Any


def parse_input(path: str) -> Dict[str, str]:
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


def print_ndjson(obj: Dict[str, Any]) -> None:
    print(json.dumps(obj, ensure_ascii=False))


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Usage: python runner.py <input_file>", file=sys.stderr)
        sys.exit(2)

    inputs = parse_input(argv[1])
    results = run(inputs)

    print(results)

if __name__ == "__main__":
    main(sys.argv)
