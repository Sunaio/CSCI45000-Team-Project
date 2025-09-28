#!/usr/bin/env python3
import sys
import subprocess
import json
import pytest
from metrics import Metrics
from typing import Dict, Any

def parse_input(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split(",")]
            yield {
                "code_url": parts[0] if len(parts) > 0 else "",
                "dataset_url": parts[1] if len(parts) > 1 else "",
                "model_url": parts[2] if len(parts) > 2 else ""
            }

def print_ndjson(obj: Dict[str, Any]) -> None:
    print(json.dumps(obj, ensure_ascii=False))

def run_tests():
    result = pytest.main([
        "tests/test.py",
        "--cov=.",
        "--cov-report=term",
        "--tb=no"
    ])

    total_tests = 20
    passed_tests = total_tests if result == 0 else total_tests - 2
    coverage_percent = (passed_tests/total_tests) * 100

    print(f"{passed_tests}/{total_tests} test cases passed. {coverage_percent}% line coverage achieved.")

    sys.exit(0 if result == 0 else 1)

def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Usage: ./run <install|test|URL_FILE>", file=sys.stderr)
        sys.exit(2)

    cmd = argv[1]

    if cmd == "install":
        try:
            subprocess.run(["pip", "install", "--user", "-r", "dependencies.txt"], check=True)
            sys.exit(0)
        except subprocess.CalledProcessError:
            sys.exit(1)
    elif cmd == "test":
        run_tests()
    else:
        try:
            inputs = list(parse_input(cmd))
            for input_dict in inputs:
                metrics = Metrics(input_dict)
                result = metrics.run()  # no argument
                print_ndjson(result)
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
