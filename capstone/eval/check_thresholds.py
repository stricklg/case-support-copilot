"""Regression gate for the capstone eval.

Reads an eval_summary.json produced by run_capstone_eval.py and
compares its headline metrics against quality floors. Prints one
PASS line per metric inside its floor and one BREACH line per
failure; exits 1 if anything breaches, so a calling process
(Kestra's check_thresholds task) fails on regression.

Usage:
    python check_thresholds.py SUMMARY_JSON ROUTING_FLOOR \
        REPLY_FLOOR TRIAGE_FLOOR

Stdlib only, like the rest of the eval harness's reporting layer.
"""
import json
import sys


def main(argv):
    if len(argv) != 5:
        print("usage: check_thresholds.py SUMMARY ROUTING_FLOOR "
              "REPLY_FLOOR TRIAGE_FLOOR")
        return 2
    with open(argv[1]) as f:
        s = json.load(f)
    checks = [
        ("routing_accuracy_pct",
         s["benchmark"]["routing_accuracy_pct"], float(argv[2])),
        ("reply_judge_overall",
         s["judge_averages"]["overall"], float(argv[3])),
        ("triage_judge_overall",
         s["triage_judge_averages"]["t_overall"], float(argv[4])),
    ]
    breaches = []
    for name, val, floor in checks:
        if val is None:
            breaches.append(name + " missing from summary")
        elif val < floor:
            breaches.append(
                "%s %.2f < floor %.2f" % (name, val, floor))
        else:
            print("PASS %s %.2f >= %.2f" % (name, val, floor))
    if s.get("triage_judged_cases", 0) == 0:
        breaches.append("triage judging produced no scores")
    for b in breaches:
        print("BREACH:", b)
    return 1 if breaches else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
