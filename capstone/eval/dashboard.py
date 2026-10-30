"""Generate a static HTML dashboard for one eval run.

Reads a reports folder (outputs.json + eval_summary.json) and
writes dashboard.html beside them: headline numbers, the routing
miss taxonomy, retrieval metrics, and both judge panels (reply
and triage). Optionally compares against a previous run's folder
for run-over-run deltas.

Usage:
  python dashboard.py reports/<ts> [--prev reports/<ts2>]
  python dashboard.py --all          (every reports folder + index)
"""

import argparse
import html
import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent

DOC2CAT = {
    "webhook_failure": "integration webhook failure",
    "billing_subscription": "billing subscription issue",
    "rate_limits": "quota/rate limit exceeded",
    "sso_provisioning": "auth/sso provisioning",
    "workflow_syntax": "workflow syntax/execution error",
    "performance_latency": "performance/latency issue",
    "data_compliance": "data export compliance",
    "feature_request": "feature request",
    "user_seats": "user/seat management",
    "onboarding_setup": "onboarding/environment setup",
}


def doc_category(doc):
    if not doc:
        return None
    name = doc.strip()
    if name.startswith("kb_"):
        name = name[3:]
    if name.endswith(".md"):
        name = name[:-3]
    return DOC2CAT.get(name.strip())


def load_run(folder):
    folder = Path(folder)
    summary = json.loads(
        (folder / "eval_summary.json").read_text())
    data = json.loads((folder / "outputs.json").read_text())
    rows = data["cases"] if isinstance(data, dict) else data
    return folder, summary, rows


def classify_miss(row, golden):
    """One-line attribution for a routing miss."""
    case = golden.get(row["case_id"], {})
    exp_cat = case.get("exp_category")
    tri = row.get("triage") or {}
    if row["status"] == 400:
        return "schema", "rejected at validation"
    if row.get("retrieved_doc") is None:
        sim = row.get("similarity")
        sim_s = f"{sim:.3f}" if isinstance(sim, float) else sim
        return "retrieval-deflect", (
            f"no runbook accepted (similarity {sim_s})")
    mapped = doc_category(row.get("retrieved_doc"))
    if (row["destination"] == "AUTOMATED_CRM"
            and case.get("exp_dest") == "HITL_QUEUE"):
        if row["category"] != exp_cat:
            return "triage-category (gate bypass)", (
                f"categorised {row['category']}, so no gate fired")
        return "dispatch", "expected HITL, automated anyway"
    if row["category"] != exp_cat and mapped == row["category"]:
        return "retrieval-wrong-doc", (
            f"retrieved {row.get('retrieved_doc')} "
            "and triage followed it")
    if row["category"] != exp_cat:
        return "triage-category", (
            f"expected {exp_cat}, got {row['category']}")
    if tri.get("secondary_categories"):
        return "multi-issue gate", (
            "also: " + ", ".join(tri["secondary_categories"]))
    margin = tri.get("retrieval_margin")
    if margin is not None and margin < 0.05:
        return "margin gate", f"margin {margin:.3f} < 0.05"
    return "dispatch-gate", "queued by confidence/escalation gate"


def retrieval_metrics(rows, golden):
    labelled = [r for r in rows if r["exp_status"] == 200
                and golden.get(r["case_id"], {}).get("exp_category")]
    matched = [r for r in labelled if r.get("retrieved_doc")]
    top_ok = sum(
        1 for r in matched
        if doc_category(r["retrieved_doc"])
        == golden[r["case_id"]]["exp_category"])
    intended_auto = [
        r for r in labelled
        if golden[r["case_id"]].get("exp_dest") == "AUTOMATED_CRM"]
    deflected_auto = [r for r in intended_auto
                      if not r.get("retrieved_doc")]
    return {
        "labelled": len(labelled),
        "matched": len(matched),
        "top_doc_pct": (round(100 * top_ok / len(matched), 1)
                        if matched else None),
        "deflect_auto": len(deflected_auto),
        "intended_auto": len(intended_auto),
    }


def esc(x):
    return html.escape(str(x))


def bar(label, value, maxv=5.0):
    pct = 0 if value is None else round(100 * value / maxv)
    shown = "n/a" if value is None else f"{value}"
    return (
        f"<tr><td>{esc(label)}</td>"
        f"<td class='barcell'><div class='bar' "
        f"style='width:{pct}%'></div></td>"
        f"<td>{shown}</td></tr>")


def build(folder, prev_folder=None):
    folder, summary, rows = load_run(folder)
    golden = {}
    cases_path = EVAL_DIR.parent / "eval" / "golden_cases.json"
    if cases_path.exists():
        data = json.loads(cases_path.read_text())
        golden = {c["id"]: c
                  for c in (data["cases"]
                            if isinstance(data, dict) else data)}
    bench = summary["benchmark"]
    rm = retrieval_metrics(rows, golden)
    misses = []
    for r in rows:
        if r["exp_status"] == 200 and r["status"] == 200 \
                and r["destination"] != r["exp_dest"]:
            cls, why = classify_miss(r, golden)
            misses.append((r["case_id"], r["exp_dest"],
                           r["destination"], cls, why))
        elif r["exp_status"] == 400 and r["status"] != 400:
            misses.append((r["case_id"], "400", r["status"],
                           "schema", "expected rejection"))
    prev_note = ""
    if prev_folder:
        _, psummary, prows = load_run(prev_folder)
        pb = psummary["benchmark"]
        changes = []
        pdest = {r["case_id"]: r["destination"] for r in prows}
        for r in rows:
            if pdest.get(r["case_id"]) != r["destination"]:
                changes.append(
                    f"{r['case_id']}: {pdest.get(r['case_id'])}"
                    f" -> {r['destination']}")
        prev_note = (
            f"<p>Routing {pb['routing_accuracy_pct']}% -> "
            f"{bench['routing_accuracy_pct']}%; reply judge "
            f"{psummary['judge_averages']['overall']} -> "
            f"{summary['judge_averages']['overall']}. "
            f"Destination changes: "
            f"{esc('; '.join(changes) if changes else 'none')}"
            f"</p>")
    reply_dims = "".join(
        bar(k, v) for k, v in summary["judge_averages"].items())
    tri_avgs = summary.get("triage_judge_averages") or {}
    tri_dims = "".join(bar(k, v) for k, v in tri_avgs.items())
    miss_rows = "".join(
        f"<tr><td>{esc(c)}</td><td>{esc(e)}</td><td>{esc(g)}"
        f"</td><td>{esc(k)}</td><td>{esc(w)}</td></tr>"
        for c, e, g, k, w in misses)
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Capstone eval - {esc(folder.name)}</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 2rem;
  color: #1c1c1e; }}
table {{ border-collapse: collapse; margin: 0.5rem 0 1.5rem; }}
td, th {{ border: 1px solid #d1d1d6; padding: 4px 10px;
  text-align: left; font-size: 14px; }}
.headline {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
.card {{ border: 1px solid #d1d1d6; border-radius: 10px;
  padding: 0.8rem 1.2rem; min-width: 130px; }}
.card .n {{ font-size: 26px; font-weight: 700; }}
.card .l {{ font-size: 12px; color: #636366; }}
.barcell {{ width: 220px; }}
.bar {{ background: #0a84ff; height: 12px; border-radius: 3px; }}
</style></head><body>
<h1>Capstone eval dashboard</h1>
<p>Run {esc(folder.name)} | mode {esc(summary['mode'])} |
generator {esc(summary['generator_model'])} | judge
{esc(summary['judge_model'])}</p>
<div class="headline">
<div class="card"><div class="n">{bench['schema_compliance_pct']}%</div>
<div class="l">schema compliance</div></div>
<div class="card"><div class="n">{bench['routing_accuracy_pct']}%</div>
<div class="l">routing accuracy</div></div>
<div class="card"><div class="n">{summary['judge_averages']['overall']}</div>
<div class="l">reply judge overall</div></div>
<div class="card"><div class="n">{summary['judge_pass_rate_at_4plus']}</div>
<div class="l">reply pass rate (&gt;= 4)</div></div>
<div class="card"><div class="n">{tri_avgs.get('t_overall')}</div>
<div class="l">triage judge overall</div></div>
<div class="card"><div class="n">{summary.get('triage_pass_rate_at_4plus')}</div>
<div class="l">triage pass rate (&gt;= 4)</div></div>
</div>
{prev_note}
<h2>Routing misses ({len(misses)})</h2>
<table><tr><th>case</th><th>expected</th><th>got</th>
<th>class</th><th>evidence</th></tr>{miss_rows}</table>
<h2>Retrieval</h2>
<p>Labelled cases: {rm['labelled']} | matched a runbook:
{rm['matched']} | top-doc accuracy: {rm['top_doc_pct']}% |
intended automations deflected: {rm['deflect_auto']} of
{rm['intended_auto']}</p>
<h2>Reply judge (n={summary['judged_cases']})</h2>
<table>{reply_dims}</table>
<p>Pass at 5: {summary['judge_pass_rate_at_5']} |
pass at &gt;= 4: {summary['judge_pass_rate_at_4plus']}</p>
<h2>Triage judge (n={summary.get('triage_judged_cases')})</h2>
<table>{tri_dims}</table>
<p>Pass at 5: {summary.get('triage_pass_rate_at_5')} |
pass at &gt;= 4: {summary.get('triage_pass_rate_at_4plus')}</p>
</body></html>
"""
    out = folder / "dashboard.html"
    out.write_text(page)
    return out


def build_all(reports_root=None):
    reports = Path(reports_root) if reports_root else \
        EVAL_DIR / "reports"
    folders = sorted(
        p for p in reports.iterdir()
        if (p / "eval_summary.json").exists())

    def _run_at(folder):
        try:
            summary = json.loads(
                (folder / "eval_summary.json").read_text())
            return summary.get("run_at", "")
        except Exception:
            return ""

    folders.sort(key=_run_at)
    prev = None
    links = []
    for f in folders:
        build(f, prev)
        links.append(f"<li><a href='{esc(f.name)}/dashboard.html'>"
                     f"{esc(f.name)}</a></li>")
        prev = f
    (reports / "index.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<title>Capstone eval runs</title></head><body>"
        "<h1>Capstone eval runs</h1><ul>"
        + "".join(links) + "</ul></body></html>")
    return len(folders)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder", nargs="?", default=None)
    ap.add_argument("--prev", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--reports-root", default=None)
    a = ap.parse_args()
    if a.all:
        print("dashboards built for",
              build_all(a.reports_root), "runs")
    else:
        print("wrote", build(Path(a.folder), a.prev))
