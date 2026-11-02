"""Dashboard builder over committed report folders,
including the guarded Costs panel: pre-instrumentation runs
must still build and must not gain a panel.
"""
import shutil
from pathlib import Path

import dashboard

REPORTS = (Path(__file__).resolve().parent.parent
           / "eval" / "reports")


def copy_run(tmp_path, name):
    dst = tmp_path / name
    shutil.copytree(REPORTS / name, dst)
    return dst


def test_dashboard_builds_for_precost_run(tmp_path):
    out = dashboard.build(copy_run(tmp_path, "20261030-160849"))
    html = out.read_text()
    assert "Capstone eval dashboard" in html
    assert "<h2>Costs</h2>" not in html


def test_dashboard_shows_costs_when_present(tmp_path):
    out = dashboard.build(copy_run(tmp_path, "20261102-171807"))
    html = out.read_text()
    assert "<h2>Costs</h2>" in html
    assert "0.3121" in html
