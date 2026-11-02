"""Run the capstone eval: pipeline benchmark + LLM-as-judge scoring.

Live mode runs every golden case through the real pipeline
(run_pipeline), captures the triage output the pipeline now exposes,
and has the OpenAI judge (judge.py) score each draft reply against
the runbook retrieval pulled for that ticket.

Replay mode re-judges the saved outputs of a previous live run
(outputs.json in a reports folder) without calling the generator.

Outputs, written to eval/reports/<timestamp>/:
  outputs.json     raw per-case pipeline outputs (replay source)
  eval_report.csv  one row per case: routing + judge scores
  eval_summary.json machine-readable run summary (the Kestra gate
                   reads this file)
  judge_report.md  human-readable summary + per-case explanations

Usage:
  python run_capstone_eval.py                 (live, built-in cases)
  python run_capstone_eval.py --mode replay --replay-from reports/<ts>
"""

import argparse
import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
CAPSTONE_DIR = EVAL_DIR.parent
sys.path.insert(0, str(CAPSTONE_DIR))
sys.path.insert(0, str(EVAL_DIR))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(CAPSTONE_DIR / ".env")

import config  # noqa: E402
import context_engine  # noqa: E402
from judge import (  # noqa: E402
    evaluate_capstone_reply, evaluate_capstone_triage,
    reset_judge_usage, take_judge_usage)

# Index-build usage captured by capture_live (live mode only).
_SETUP_USAGE = {'embed': None, 'gen': None}
from rubrics import RUBRIC_CAPSTONE, RUBRIC_TRIAGE  # noqa: E402


def load_cases(cases_path):
    """Golden cases: JSON file if given, else the set in main.py."""
    if cases_path:
        data = json.loads(Path(cases_path).read_text())
        return data["cases"] if isinstance(data, dict) else data
    import main as capstone_main

    return capstone_main.GOLDEN_EVAL_SET


def ticket_text(payload):
    return (payload.get("subject", "") + "\n\n"
            + payload.get("body", "")).strip()


def capture_live(cases):
    """Run each case through the pipeline; return JudgeCase dicts."""
    import main as capstone_main
    import context_engine
    from context_engine import KB

    capstone_main.reset_usage()
    context_engine.reset_embed_usage()
    kb = KB(kb_dir=CAPSTONE_DIR / "kb")
    kb.build_index()
    _SETUP_USAGE['embed'] = context_engine.take_embed_usage()
    _SETUP_USAGE['gen'] = capstone_main.take_usage()
    captured = []
    for case in cases:
        payload = case["payload"]
        capstone_main.reset_usage()
        context_engine.reset_embed_usage()
        status, res = capstone_main.run_pipeline(payload, kb)
        row = {
            "case_id": case["id"],
            "ticket_text": ticket_text(payload),
            "exp_status": case["exp_status"],
            "exp_dest": case.get("exp_dest"),
            "status": status,
            "destination": None,
            "category": None,
            "draft_reply": None,
            "retrieved_doc": None,
            "retrieved_content": None,
            "similarity": None,
            "latency_ms": None,
            "triage": None,
        }
        if status == 200:
            dest = res["execution"]["destination"]
            row["destination"] = getattr(dest, "value", str(dest))
            row["category"] = res["triage"]["category"]
            row["triage"] = res["triage"]
            row["draft_reply"] = res["triage"]["draft_reply"]
            row["retrieved_doc"] = res["retrieval"]["matched_kb"]
            row["retrieved_content"] = (
                res["retrieval"]["matched_content"])
            row["similarity"] = res["retrieval"]["similarity_score"]
            row["latency_ms"] = res.get("total_latency_ms")
        row["usage"] = {
            "gen": capstone_main.take_usage(),
            "embed": context_engine.take_embed_usage(),
        }
        captured.append(row)
    return captured


def judge_rows(rows):
    """Judge every row that produced a real reply. Adds score keys."""
    for row in rows:
        reset_judge_usage()
        row["judged"] = False
        row["triage_judged"] = False
        if (row["status"] == 200 and row["draft_reply"]
                and row["retrieved_content"]):
            result = evaluate_capstone_reply(
                row["ticket_text"], row["draft_reply"],
                RUBRIC_CAPSTONE, kb_context=row["retrieved_content"],
            )
            row.update({
                "judged": True,
                "groundedness": result.groundedness,
                "accuracy": result.accuracy,
                "actionability": result.actionability,
                "tone": result.tone,
                "overall": result.overall,
                "passed": result.passed,
                "judge_explanation": result.explanation,
            })
        if row["judged"] and row.get("triage"):
            t = evaluate_capstone_triage(
                row["ticket_text"], row["triage"], RUBRIC_TRIAGE)
            row.update({
                "triage_judged": True,
                "t_category_fit": t.category_fit,
                "t_priority_calibration": t.priority_calibration,
                "t_action_needed": t.action_needed,
                "t_issue_completeness": t.issue_completeness,
                "t_overall": t.overall,
                "t_passed": t.passed,
                "t_judge_explanation": t.explanation,
            })
        row["judge_usage"] = take_judge_usage()
    return rows


def benchmark(rows):
    total = len(rows)
    schema = sum(1 for r in rows if r["status"] == r["exp_status"])
    routing = 0
    for r in rows:
        dest = r.get("destination") or ""
        if "." in dest:
            dest = dest.rsplit(".", 1)[-1]
        if r["status"] == 400 and r["exp_status"] == 400:
            routing += 1
        elif r["status"] == 200 and dest == r["exp_dest"]:
            routing += 1
    return {
        "cases": total,
        "schema_compliance_pct": round(100 * schema / total, 1),
        "routing_accuracy_pct": round(100 * routing / total, 1),
    }


def _gen_usd(gen):
    total = 0.0
    for model, b in (gen.get("by_model") or {}).items():
        price = config.PRICES.get(model)
        if price is None:
            continue
        out = b["output_tokens"] + b["thoughts_tokens"]
        total += (b["prompt_tokens"] * price["input"]
                  + out * price["output"]) / 1_000_000
    return total


def _embed_usd(tokens):
    price = config.PRICES[config.EMBEDDING_MODEL]
    return tokens * price["input"] / 1_000_000


def _judge_usd(ju):
    price = config.PRICES[config.JUDGE_MODEL]
    return (ju["input_tokens"] * price["input"]
            + ju["output_tokens"] * price["output"]) / 1_000_000


def _build_costs(rows, mode):
    """Assemble the costs block for eval_summary.json.

    Token counts are measured (Gemini usage_metadata, OpenAI
    usage, count_tokens for embeddings); USD comes from
    config.PRICES as of config.PRICES_AS_OF. Per-ticket
    production cost counts generation + query embeddings
    only - judging and index build are eval/setup spend and
    stay in their own buckets. Replay mode never re-runs the
    generator, so its fields are null, not zero.
    """
    costs = {
        "prices_as_of": config.PRICES_AS_OF,
        "currency": "USD",
        "tokens_estimated": False,
    }
    ju_all = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    for r in rows:
        ju = r.get("judge_usage") or {}
        for k in ju_all:
            ju_all[k] += ju.get(k, 0)
    judge_usd = _judge_usd(ju_all)
    costs["judge"] = dict(ju_all, usd=round(judge_usd, 4))
    if mode != "live":
        costs["generator"] = None
        costs["query_embeddings"] = None
        costs["setup_index_build"] = None
        costs["per_ticket_usd"] = None
        costs["run_total_usd"] = None
        costs["kestra_daily_projection_usd_30d"] = None
        costs["not_measured"] = (
            "replay mode: generator and embedding calls are "
            "not re-run, so their costs are not measured; "
            "judge costs above are measured live")
        return costs
    gen_all = {"calls": 0, "prompt_tokens": 0,
               "output_tokens": 0, "thoughts_tokens": 0}
    gen_usd = 0.0
    emb_calls = 0
    emb_tokens = 0
    groups = {"automated": [], "deflected": [], "human_queue": []}
    for r in rows:
        usage = r.get("usage") or {}
        gen = usage.get("gen") or {}
        emb = usage.get("embed") or {}
        for k in gen_all:
            gen_all[k] += gen.get(k, 0)
        row_gen_usd = _gen_usd(gen)
        gen_usd += row_gen_usd
        emb_calls += emb.get("calls", 0)
        emb_tokens += emb.get("tokens", 0)
        if r["status"] != 200:
            continue
        ticket_usd = row_gen_usd + _embed_usd(emb.get("tokens", 0))
        dest = r.get("destination") or ""
        if "." in dest:
            dest = dest.rsplit(".", 1)[-1]
        if dest == "AUTOMATED_CRM":
            groups["automated"].append(ticket_usd)
        elif gen.get("calls", 0) == 0:
            groups["deflected"].append(ticket_usd)
        else:
            groups["human_queue"].append(ticket_usd)
    setup_emb = _SETUP_USAGE.get("embed") or {}
    setup_usd = _embed_usd(setup_emb.get("tokens", 0))
    costs["generator"] = dict(gen_all, usd=round(gen_usd, 4))
    costs["query_embeddings"] = {
        "calls": emb_calls, "tokens": emb_tokens,
        "usd": round(_embed_usd(emb_tokens), 4)}
    costs["setup_index_build"] = {
        "embedding_calls": setup_emb.get("calls", 0),
        "tokens": setup_emb.get("tokens", 0),
        "usd": round(setup_usd, 4)}
    costs["per_ticket_usd"] = {
        name: {"n": len(vals),
               "mean": (round(sum(vals) / len(vals), 6)
                        if vals else None)}
        for name, vals in groups.items()}
    run_total = (setup_usd + gen_usd + _embed_usd(emb_tokens)
                 + judge_usd)
    costs["run_total_usd"] = round(run_total, 4)
    costs["kestra_daily_projection_usd_30d"] = round(
        run_total * 30, 2)
    return costs


def summarise(rows, bench, mode):
    judged = [r for r in rows if r.get("judged")]
    dims = ["groundedness", "accuracy", "actionability", "tone",
            "overall"]
    avgs = {}
    for d in dims:
        avgs[d] = (round(sum(r[d] for r in judged) / len(judged), 2)
                   if judged else None)
    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "generator_model": config.PRIMARY_MODEL,
        "fallback_model": config.FALLBACK_MODEL,
        "judge_model": config.JUDGE_MODEL,
        "similarity_threshold": config.SIMILARITY_THRESHOLD,
        "confidence_threshold": config.CONFIDENCE_THRESHOLD,
        "benchmark": bench,
        "judged_cases": len(judged),
        "judge_averages": avgs,
        "judge_pass_rate_at_5": (
            round(sum(1 for r in judged if r["overall"] == 5)
                  / len(judged), 3) if judged else None),
        "judge_pass_rate_at_4plus": (
            round(sum(1 for r in judged if r["overall"] >= 4)
                  / len(judged), 3) if judged else None),
    }
    tjudged = [r for r in rows if r.get("triage_judged")]
    tdims = ["t_category_fit", "t_priority_calibration",
             "t_action_needed", "t_issue_completeness", "t_overall"]
    summary["triage_judged_cases"] = len(tjudged)
    summary["triage_judge_averages"] = {
        d: (round(sum(r[d] for r in tjudged) / len(tjudged), 2)
            if tjudged else None) for d in tdims}
    summary["triage_pass_rate_at_4plus"] = (
        round(sum(1 for r in tjudged if r["t_overall"] >= 4)
              / len(tjudged), 3) if tjudged else None)
    summary["triage_pass_rate_at_5"] = (
        round(sum(1 for r in tjudged if r["t_overall"] == 5)
              / len(tjudged), 3) if tjudged else None)
    summary["costs"] = _build_costs(rows, mode)
    return summary


def write_outputs(rows, summary, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "outputs.json").write_text(json.dumps(
        {"summary": summary, "cases": rows}, indent=2))
    fields = ["case_id", "status", "exp_status", "destination",
              "exp_dest", "category", "retrieved_doc", "similarity",
              "judged", "groundedness", "accuracy", "actionability",
              "tone", "overall", "passed", "judge_explanation",
              "triage_judged", "t_category_fit",
              "t_priority_calibration", "t_action_needed",
              "t_issue_completeness", "t_overall", "t_passed",
              "t_judge_explanation"]
    with open(out_dir / "eval_report.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields,
                                extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    (out_dir / "eval_summary.json").write_text(
        json.dumps(summary, indent=2))
    lines = [
        "# Capstone eval report",
        "",
        f"Run at: {summary['run_at']} (mode: {summary['mode']})",
        f"Generator: {summary['generator_model']} "
        f"(fallback {summary['fallback_model']}) | "
        f"Judge: {summary['judge_model']}",
        "",
        "## Benchmark",
        f"- Schema compliance: "
        f"{summary['benchmark']['schema_compliance_pct']}%",
        f"- Routing accuracy: "
        f"{summary['benchmark']['routing_accuracy_pct']}%",
        "",
        "## Judge (draft replies)",
        f"- Cases judged: {summary['judged_cases']}",
    ]
    for dim, avg in summary["judge_averages"].items():
        lines.append(f"- Avg {dim}: {avg}")
    lines.append(f"- Pass rate (overall = 5): "
                 f"{summary['judge_pass_rate_at_5']}")
    lines.append(f"- Pass rate (overall >= 4): "
                 f"{summary['judge_pass_rate_at_4plus']}")
    lines += ["", "## Judge (triage decisions)",
              f"- Cases judged: {summary['triage_judged_cases']}"]
    for dim, avg in summary["triage_judge_averages"].items():
        lines.append(f"- Avg {dim}: {avg}")
    lines.append(f"- Pass rate (overall >= 4): "
                 f"{summary['triage_pass_rate_at_4plus']}")
    lines.append(f"- Pass rate (overall = 5): "
                 f"{summary['triage_pass_rate_at_5']}")
    costs = summary.get("costs")
    if costs:
        lines += ["", "## Costs",
                  f"Prices as of {costs['prices_as_of']} "
                  f"({costs['currency']}); token counts measured, "
                  "not estimated."]
        if costs.get("run_total_usd") is not None:
            lines.append(f"- Run total: ${costs['run_total_usd']}")
            lines.append(
                f"- Generator: ${costs['generator']['usd']} | "
                f"Judge: ${costs['judge']['usd']} | "
                f"Embeddings (queries): "
                f"${costs['query_embeddings']['usd']} | "
                f"Index build: "
                f"${costs['setup_index_build']['usd']}")
            for name, g in costs["per_ticket_usd"].items():
                lines.append(f"- Per ticket ({name}): "
                             f"mean ${g['mean']} (n={g['n']})")
            lines.append(
                "- Kestra daily projection (30d): "
                f"${costs['kestra_daily_projection_usd_30d']}")
        else:
            lines.append(f"- Judge (measured live): "
                         f"${costs['judge']['usd']}")
            lines.append(f"- {costs['not_measured']}")
    lines += ["", "## Per-case judge notes", ""]
    for r in rows:
        if r.get("judged"):
            lines.append(f"### {r['case_id']} — overall {r['overall']}"
                         f" (passed: {r['passed']})")
            lines.append(f"Retrieved: {r['retrieved_doc']} | "
                         f"Category: {r['category']} | "
                         f"Destination: {r['destination']}")
            lines.append("")
            lines.append(r["judge_explanation"])
            if r.get("triage_judged"):
                lines.append(f"Triage: overall {r['t_overall']} "
                             f"(passed: {r['t_passed']}) - "
                             f"{r['t_judge_explanation']}")
            lines.append("")
        else:
            lines.append(f"### {r['case_id']} — not judged "
                         f"(status {r['status']}, "
                         f"destination {r['destination']})")
            lines.append("")
    (out_dir / "judge_report.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["live", "replay"],
                        default="live")
    parser.add_argument("--cases", default=None,
                        help="JSON file of golden cases")
    parser.add_argument("--replay-from", default=None,
                        help="reports folder to re-judge (replay mode)")
    parser.add_argument("--out", default=None,
                        help="output folder (default reports/<ts>)")
    parser.add_argument("--keep-telemetry", action="store_true",
                        help="do not restore telemetry_events.jsonl")
    args = parser.parse_args()

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out) if args.out else (
        EVAL_DIR / "reports" / stamp)

    telemetry = CAPSTONE_DIR / "telemetry_events.jsonl"
    backup = None
    if args.mode == "live" and not args.keep_telemetry \
            and telemetry.exists():
        backup = telemetry.with_suffix(".jsonl.evalbak")
        shutil.copy(telemetry, backup)
    try:
        if args.mode == "live":
            cases = load_cases(args.cases)
            rows = capture_live(cases)
        else:
            source = Path(args.replay_from) / "outputs.json"
            rows = json.loads(source.read_text())["cases"]
        rows = judge_rows(rows)
        summary = summarise(rows, benchmark(rows), args.mode)
        write_outputs(rows, summary, out_dir)
    finally:
        if backup is not None and telemetry.exists():
            shutil.move(str(backup), str(telemetry))
    print(json.dumps(summary, indent=2))
    print("Reports written to", out_dir)


if __name__ == "__main__":
    main()
