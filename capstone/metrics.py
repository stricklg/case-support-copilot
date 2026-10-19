import json
from collections import defaultdict
from pathlib import Path
import numpy as np


def analyze_telemetry(
    LOG_FILE_PATH = Path(__file__).resolve().parent / "telemetry_events.jsonl"
):
  path = Path(LOG_FILE_PATH)
  if not path.exists():
    print(f"Error: Log file '{LOG_FILE_PATH}' not found.")
    return

  latencies_by_stage = defaultdict(list)
  destinations = defaultdict(int)
  total_retrieval_events = 0
  deflected_retrieval_events = 0
  stage_counts = defaultdict(int)

  with open(path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
      line = line.strip()
      if not line:
        continue
      try:
        event = json.loads(line)
      except json.JSONDecodeError:
        print(f"Skipping malformed JSON on line {line_num}")
        continue

      stage = event.get("stage", "UNKNOWN")
      status = event.get("status", "UNKNOWN")
      latency = event.get("latency_ms")
      details = event.get("details", {})

      stage_counts[stage] += 1

      # Record stage latency
      if latency is not None:
        latencies_by_stage[stage].append(float(latency))

      # Track retrieval gating and deflections
      if stage == "RETRIEVAL":
        total_retrieval_events += 1
        is_deflected = (
          status == "DEFLECTED"
          or details.get("deflected") is True
          or details.get("matched") is False
          or details.get("doc_name") is None
        )
        if is_deflected:
          deflected_retrieval_events += 1

      # Track downstream execution routing distribution
      if stage == "EXECUTION" and status == "SUCCESS":
        dest = details.get("destination", "UNKNOWN")
        destinations[dest] += 1

  # Latency Summary (p50 / p95)
  print("\n" + "=" * 60)
  print("             STAGE LATENCY PERFORMANCE (ms)                  ")
  print("=" * 60)
  print(f"{'Stage':<15} {'Samples':<10} {'p50 (Median)':<15} {'p95':<15}")
  print("-" * 60)

  for stage, latencies in sorted(latencies_by_stage.items()):
    if not latencies:
      continue
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    print(f"{stage:<15} {len(latencies):<10} {p50:<15.2f} {p95:<15.2f}")

  # Deflection Metrics
  print("\n" + "=" * 60)
  print("             RETRIEVAL GATING & DEFLECTION                   ")
  print("=" * 60)
  if total_retrieval_events > 0:
    deflection_pct = (
        deflected_retrieval_events / total_retrieval_events
    ) * 100
    matched_events = total_retrieval_events - deflected_retrieval_events
    print(f"Total In-Scope Evaluation Inquiries: {total_retrieval_events}")
    print(
        f"Deflected (Below Similarity Gate):   {deflected_retrieval_events}"
        f" ({deflection_pct:.1f}%)"
    )
    print(
        f"Matched & Passed to Triage:          {matched_events}"
        f" ({100 - deflection_pct:.1f}%)"
    )
  else:
    print("No RETRIEVAL stage events found in telemetry.")

  # Execution Destination Distribution
  print("\n" + "=" * 60)
  print("             DOWNSTREAM ROUTING DISTRIBUTION                 ")
  print("=" * 60)
  total_executions = sum(destinations.values())
  if total_executions > 0:
    for dest, count in sorted(
        destinations.items(), key=lambda x: x[1], reverse=True
    ):
      share = (count / total_executions) * 100
      print(f"{dest:<25} {count:<5} ({share:.1f}%)")
  else:
    print("No EXECUTION stage events found in telemetry.")

  print("=" * 60 + "\n")


if __name__ == "__main__":
  analyze_telemetry()
