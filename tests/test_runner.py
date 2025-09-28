import sys
import json
import types
from pathlib import Path
import runner


class FakeMetrics(types.ModuleType):
    def run_all(self, inputs):
        return [
            {"metric": "license", "score": 1, "details": {"license": "MIT"}},
            {"metric": "size", "score": 0, "details": {"loc": 123}},
        ]


def test_runner_output(tmp_path, capsys, monkeypatch):
    sys.modules["metrics"] = FakeMetrics("metrics")
    input_file = tmp_path / "input.txt"
    input_file.write_text("code_url,dataset_url,model_url")

    runner.main(["runner", str(input_file)])
    out_lines = capsys.readouterr().out.strip().splitlines()
    rows = [json.loads(line) for line in out_lines]

    names = [r["metric"] for r in rows]
    assert "latency_ok" in names
    assert "license" in names
    assert "size" in names
    for r in rows:
        assert r["score"] in (0, 1)
