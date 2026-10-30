#!/bin/sh
# Runs INSIDE the eval container (python:3.12-slim), which the
# Kestra flow creates through the Docker socket API with the repo
# mounted read-only at /src and the workdir at /workdir.
# $1 = run id (the Kestra execution id) - namespaces this run's
# copy of the capstone and its report folder in the archive.
set -e
RUN_ID="$1"
mkdir -p /workdir/runs/$RUN_ID /workdir/eval-archive
cp -r /src/capstone /workdir/runs/$RUN_ID/capstone
pip install --quiet \
  -r /workdir/runs/$RUN_ID/capstone/eval/requirements-eval.txt
cd /workdir/runs/$RUN_ID/capstone
python eval/run_capstone_eval.py \
  --cases eval/golden_cases.json \
  --out /workdir/eval-archive/$RUN_ID
