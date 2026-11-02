"""Regression-gate CLI (eval/check_thresholds.py).

The exit code is the contract the Kestra pipeline depends
on: 0 = all floors pass, 1 = breach (the execution fails).
"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = (Path(__file__).resolve().parent.parent
          / "eval" / "check_thresholds.py")

BASE = {
    "benchmark": {"routing_accuracy_pct": 86.0},
    "judge_averages": {"overall": 3.27},
    "triage_judge_averages": {"t_overall": 4.42},
    "triage_judged_cases": 33,
}


def run_gate(tmp_path, summary):
    f = tmp_path / "summary.json"
    f.write_text(json.dumps(summary))
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(f),
         "80", "2.7", "3.8"],
        capture_output=True, text=True)


def variant(**changes):
    data = json.loads(json.dumps(BASE))
    for key, value in changes.items():
        data[key] = value
    return data


def test_gate_passes_at_baseline(tmp_path):
    r = run_gate(tmp_path, BASE)
    assert r.returncode == 0
    assert r.stdout.count("PASS") == 3


def test_gate_breaches_on_low_routing(tmp_path):
    bad = variant(benchmark={"routing_accuracy_pct": 79.9})
    r = run_gate(tmp_path, bad)
    assert r.returncode == 1
    assert "BREACH" in r.stdout


def test_gate_breaches_when_triage_never_judged(tmp_path):
    bad = variant(triage_judged_cases=0)
    r = run_gate(tmp_path, bad)
    assert r.returncode == 1
