"""Cost instrumentation: pricing math, the usage
accumulators, and the runner's costs block.

Expectations are hand-computed from config.PRICES - the same
arithmetic verified against the first instrumented live run
(reports/20261102-171807).
"""
import pytest

import config
import context_engine
import judge
import main
import run_capstone_eval as runner


def test_price_table_covers_every_model():
    for model in (config.PRIMARY_MODEL, config.FALLBACK_MODEL,
                  config.EMBEDDING_MODEL, config.JUDGE_MODEL):
        assert model in config.PRICES
        assert config.PRICES[model]["input"] > 0


def test_gen_usd_bills_thoughts_at_output_rate():
    gen = {"by_model": {"gemini-3.5-flash-lite": {
        "calls": 1, "prompt_tokens": 2000,
        "output_tokens": 300, "thoughts_tokens": 50}}}
    # (2000 x 0.30 + 350 x 2.50) / 1e6
    assert runner._gen_usd(gen) == pytest.approx(0.001475)


def test_gen_usd_unknown_model_is_skipped():
    gen = {"by_model": {"some-future-model": {
        "calls": 1, "prompt_tokens": 1000,
        "output_tokens": 1000, "thoughts_tokens": 0}}}
    assert runner._gen_usd(gen) == 0.0


def test_judge_and_embed_usd():
    ju = {"input_tokens": 3000, "output_tokens": 400}
    # (3000 x 2.00 + 400 x 10.00) / 1e6
    assert runner._judge_usd(ju) == pytest.approx(0.01)
    assert runner._embed_usd(10000) == pytest.approx(0.0015)


def test_usage_accumulators_reset_and_take():
    main.reset_usage()
    main.USAGE_TOTALS["calls"] = 3
    assert main.take_usage()["calls"] == 3
    assert main.USAGE_TOTALS["calls"] == 0
    context_engine.reset_embed_usage()
    context_engine.EMBED_USAGE["tokens"] = 42
    assert context_engine.take_embed_usage()["tokens"] == 42
    assert context_engine.EMBED_USAGE["tokens"] == 0
    judge.reset_judge_usage()
    judge.JUDGE_USAGE["calls"] = 2
    assert judge.take_judge_usage()["calls"] == 2
    assert judge.JUDGE_USAGE["calls"] == 0


def _rows():
    gen = {"calls": 1, "prompt_tokens": 2000,
           "output_tokens": 300, "thoughts_tokens": 50,
           "by_model": {"gemini-3.5-flash-lite": {
               "calls": 1, "prompt_tokens": 2000,
               "output_tokens": 300, "thoughts_tokens": 50}}}
    empty = {"calls": 0, "prompt_tokens": 0, "output_tokens": 0,
             "thoughts_tokens": 0, "by_model": {}}
    zero_judge = {"calls": 0, "input_tokens": 0,
                  "output_tokens": 0}
    return [
        {"status": 200, "destination": "AUTOMATED_CRM",
         "usage": {"gen": gen,
                   "embed": {"calls": 2, "tokens": 100}},
         "judge_usage": {"calls": 2, "input_tokens": 3000,
                         "output_tokens": 400}},
        {"status": 200, "destination": "HITL_QUEUE",
         "usage": {"gen": empty,
                   "embed": {"calls": 2, "tokens": 90}},
         "judge_usage": zero_judge},
        {"status": 400, "destination": None,
         "usage": {"gen": empty,
                   "embed": {"calls": 0, "tokens": 0}},
         "judge_usage": zero_judge},
    ]


def test_build_costs_live():
    runner._SETUP_USAGE["embed"] = {"calls": 31,
                                    "tokens": 5000}
    costs = runner._build_costs(_rows(), "live")
    assert costs["judge"]["usd"] == pytest.approx(0.01)
    assert costs["generator"]["usd"] == pytest.approx(0.0015)
    per = costs["per_ticket_usd"]
    assert per["automated"]["mean"] == pytest.approx(0.00149)
    assert per["deflected"]["n"] == 1
    assert per["human_queue"]["n"] == 0
    assert costs["run_total_usd"] == pytest.approx(0.0123)
    assert costs["kestra_daily_projection_usd_30d"] == \
        pytest.approx(0.37)


def test_build_costs_replay_never_invents_generator_costs():
    costs = runner._build_costs(_rows(), "replay")
    assert costs["generator"] is None
    assert costs["run_total_usd"] is None
    assert costs["judge"]["usd"] == pytest.approx(0.01)
    assert "not re-run" in costs["not_measured"]


def test_benchmark_counts_schema_and_routing():
    rows = [
        {"status": 200, "exp_status": 200,
         "destination": "AUTOMATED_CRM",
         "exp_dest": "AUTOMATED_CRM"},
        {"status": 400, "exp_status": 200,
         "destination": None, "exp_dest": "AUTOMATED_CRM"},
        {"status": 400, "exp_status": 400,
         "destination": None, "exp_dest": "HITL_QUEUE"},
    ]
    bench = runner.benchmark(rows)
    assert bench["cases"] == 3
    assert bench["schema_compliance_pct"] == \
        pytest.approx(66.7)
    assert bench["routing_accuracy_pct"] == \
        pytest.approx(66.7)
