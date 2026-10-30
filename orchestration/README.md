# Orchestration: Kestra eval pipeline

`capstone_eval_pipeline.yml` is the Kestra flow that runs the
capstone eval as a regression gate. It is the third tier of the
portfolio: the capstone is the product, `capstone/eval/` is its
measurement harness, and this flow is the scheduled orchestration
and observability layer around that harness. It orchestrates
evaluation - it is not an autonomous agent.

**This YAML is the source of truth.** The Kestra instance on the
dev PC is created from this file; after editing here, re-import
the flow (Kestra UI: Flows -> the flow -> Edit -> paste, or the
API) so the running copy matches the repo.

## What one execution does

1. `run_eval` - copies `capstone/` out of this repo (mounted
   read-only) into a scratch workdir, installs the minimal eval
   dependencies (`capstone/eval/requirements-eval.txt`), and runs
   the full 50-case eval: pipeline + reply judge + triage judge.
   The in-container steps live in `orchestration/run_eval.sh`.
   Reports land in the workdir archive, never back in the repo -
   a scheduled job writing into the working tree would fight the
   commit discipline, and the reports are regenerable artifacts.
2. `build_dashboard` - generates the run's `dashboard.html` and
   rebuilds the archive-wide `index.html`.
3. `check_thresholds` - the regression gate.
   `capstone/eval/check_thresholds.py` reads the run's
   `eval_summary.json` and exits non-zero on any breach, which
   fails the execution; Kestra's execution history is the
   observability trail.

## Execution model: containers via the Docker socket API

Each task is a shell task on Kestra's process runner whose
commands create a throwaway `python:3.12-slim` container through
the Docker socket API (`curl --unix-socket`), passing explicit
bind mounts, streaming the container's logs back into the task
log, and exiting with the container's exit code.

Why not Kestra's container task types? In this install
(Kestra 1.3.21), both the scripts Docker task runner and the
docker plugin's Run task accept a `volumes` property, validate
it, and store it - and then create containers with no binds at
all. Verified 2026-10-30 across three probes: the task
containers report `/src` missing, and `docker inspect` on a
live task container shows `Binds: null`, while the same bind
strings work under a plain `docker run`. Rather than fight the
layer, the flow drives the daemon's API directly, where the
binds are explicit in the create payload. Kestra still provides
everything the tier exists for: scheduling, secret injection,
per-task logs, and pass/fail execution history.

## Gate floors (flow variables, editable in the Kestra UI)

| Metric | Floor | Baseline 2026-10-30 |
| --- | --- | --- |
| Routing accuracy | >= 80% | 86% |
| Reply judge overall | >= 2.7 | 3.06 |
| Triage judge overall | >= 3.8 | 4.18 |

Each floor sits about two noise-widths below its baseline: tight
enough to catch a cliff, loose enough not to fire on judge
variance. The triage gate also fails if triage judging produced
no scores at all - a silently-dead judge must not pass as green.

## Schedule: daily, currently OFF

The flow carries a Schedule trigger for 07:00 America/Denver
daily, **disabled**. Every run makes ~50 generator calls and
~66 judge calls against paid APIs, so the cadence stays off
until it is deliberately enabled (edit the flow and set the
trigger's `disabled` to false, here and in Kestra). Manual
executions from the Kestra UI work at any time.

## Layout on the dev PC

- Repo: `~/dev/capstone-public` (mounted read-only into the
  eval containers at `/src`)
- Workdir: `~/dev/kestra-wd` (mounted at `/workdir`)
  - `runs/<execution-id>/capstone/` - the per-run repo copy
  - `eval-archive/<execution-id>/` - report + `dashboard.html`
  - `eval-archive/index.html` - dashboard index across runs

The workdir deliberately lives under the home directory, not
`/tmp`: `/tmp` is periodically cleaned, which would silently
break the archive.

## Secrets

The flow reads `GEMINI_API_KEY` and `OPENAI_API_KEY` through
Kestra's `secret()` from the server environment
(`SECRET_GEMINI_API_KEY`, `SECRET_OPENAI_API_KEY` in
`~/dev/kestra/.env`, base64-encoded), and forwards them into
the eval container by name. Keys never appear in this repo or
in the flow file.
