# Failure: the knowledge base that indexed 8 of 10 documents

## Observed

The pipeline indexed its knowledge base and reported success — "Indexing N KB's…
Vector store indexing complete" — and the golden benchmark passed 10/10. But
billing and SSO tickets never matched a runbook. They scored below the 0.65
similarity gate every time and deflected to the human queue, as if the runbooks
for those two categories didn't exist.

They did exist. Both files were sitting in `capstone/kb/` the whole time.

## Isolation

`build_index()` in `context_engine.py` finds runbooks with:

```python
files = list(self.kb_dir.rglob("*.md"))
```

Listing what that glob actually returned, instead of what the directory
appeared to contain, showed 8 files — not 10. Inspecting the two missing
filenames byte-by-byte found the cause: both carried a trailing invisible
Unicode character, **U+2060 (WORD JOINER), after the `.md` extension** —
an artifact of how the files came out of a Codespaces export. The filenames
*rendered* as `kb_ billing_subscription.md` and `kb_ sso_provisioning.md`,
but on disk they ended `...md⁠`, so `*.md` never matched them.

The benchmark mostly couldn't catch this: the 10-case golden set
contains no billing case and no SSO *automation* case. It does contain
an SSO *escalation* case (G09, expected: human queue) — and that case
was passing only because of the bug. With the SSO runbook unindexed,
G09 deflected to the human queue by accident, which is the destination
the test expected, for entirely the wrong reason. The "100% routing
accuracy" was true over a test set that never exercised the broken
categories as automations — and one of its passes was an artifact of
the bug itself.

## Decision

Rename the files, don't loosen the code:

1. First checked that nothing referenced the filenames — code, docs, and
   telemetry only use the *category* strings (`billing_subscription_issue`,
   `auth_sso_provisioning`), never the file paths. A rename was safe.
2. `git mv` both files, stripping only the trailing U+2060 — no content
   changes (Git records both as pure renames, R100).

The alternative — making the glob tolerant of trailing characters — was
rejected: it would have hidden a data-integrity problem inside retrieval
code, and the next export artifact would have failed differently.

## Verification

- The index now builds from **10 documents**, not 8.
- A live Okta/SAML query that previously deflected now matches
  `kb_ sso_provisioning.md` at **0.749** similarity.
- The rename commit contains no content changes.
- Re-running the golden benchmark against the fixed index (2026-10-26):
  **Schema Compliance 100% (10/10), Routing Accuracy 90% (9/10)** —
  down from the 100% recorded against the 8-document index. The one
  miss is G09, and it is not a regression: see "What it exposed."

Committed as `8fa365e` — "Fix invisible character in billing and SSO KB
filenames so all 10 docs index" (in this public repo: `4f40333`).

## What it exposed

Fixing the filenames didn't make billing robust — it made it *measurable*.
With the billing runbook actually indexed, three clearly-billing phrasings
score **0.702 / 0.635 / 0.631** against the 0.65 gate: two of three would
still deflect. That's whole-document, single-vector embedding diluting a
long runbook — a threshold/chunking problem the bug had been masking.

Fixing the index also exposed why G09 misroutes now. With its runbook
indexed, G09 matches at 0.715 and auto-routes to the CRM instead of the
human queue. It should have been caught by the escalation gate in
`actions.py` — SSO is meant to always get human review — but the gate
never fires: `ESCALATION_CATEGORIES` holds human-readable labels
("sso configuration", "custom export", "feature request") while
triage emits snake_case category IDs (`auth_sso_provisioning`). The
membership test compares two vocabularies and matches neither, so
routing is decided by the similarity score alone. That is a second,
distinct bug — in the dispatch logic, not the index — and the indexing
bug had been hiding it by keeping SSO tickets away from the gate
entirely.

Follow-ups, tracked in the eval work:

- Align `ESCALATION_CATEGORIES` with the triage category IDs, and add a
  golden case that proves the escalation gate fires.
- The golden set grows from 10 to 50 cases, with billing and SSO cases
  included specifically because the original set's blind spot hid this.
- A benchmark that passes 100% is a statement about the test set, not
  the system. Scores get quoted with the date and the index state they
  were measured against; coverage gets reviewed before scores get
  quoted.
