# Case Support Copilot

A RAG-grounded support-triage system: it validates an incoming ticket, retrieves the
matching runbook from a knowledge base, has an LLM classify and draft a grounded reply, and
routes the ticket to an automated handling queue or a human review queue. Telemetry exists
at every step, alongside an LLM-as-judge eval harness for reply quality — a daily automated
run of that harness via Kestra is planned; today it runs on demand.

This was built for a fictional SaaS company ("OmniFlow") as a portfolio capstone. It
demonstrates defensive ingestion, a retrieval gate that can refuse to answer, tiered
inference with fallback, and measured routing.

Not included: a real CRM system at the end — the dispatch targets are mocks (see Limitations).

## The problem

Support triage is repetitive and can take up a lot of work hours, but automation with AI
can be risky and potentially costly. An LLM that answers from memory can invent policies
(hallucinate). An AI system can waste tokens (processing capital) responding to
out-of-scope inquiries. This system only lets the model draft from an approved knowledge
base, deflects tickets without a knowledge base match to a human (preserving tokens), and
escalates categories that should never be automated (feature requests, SSO/security,
custom exports) regardless of LLM confidence.

## How it works

```
Ticket (JSON)
  → 1. Ingestion    Pydantic InboundTicket validates + normalizes; a malformed ticket never reaches a model
  → 2. Retrieval    Ticket text embedded (gemini-embedding-001); cosine vs. 10 knowledge base documents;
                    best score < 0.65 → deflected to human queue, no LLM call
  → 3. Triage       Gemini 3.5 Flash-Lite drafts category / priority / reply from the
                    retrieved knowledge base only (temperature 0, strict JSON schema);
                    on API error only, falls back to Gemini 3.8 Flash
  → 4. Dispatch     Confidence ≥ 0.65 and category not in the always-escalate set
                    → AUTOMATED_CRM (mock); otherwise → HITL queue + SLA notice
  → 5. Telemetry    Append-only JSONL event at every boundary; metrics.py reports
                    p50/p95 latency, deflection, and routing distribution
```

## Architecture Diagram
```mermaid
flowchart TD
    %% Node Definitions & Shapes
    USER([User / Ticket Ingestion])
    
    subgraph Ingestion ["1. Defensive Ingestion & Sanitization"]
        P_IN{Pydantic Inbound Contract}
        CLEAN[Whitespace Strip & Normalization]
        IN_REJECT[Reject & Alert Source: 400 Bad Request]
    end

    subgraph Retrieval ["2. Grounded Retrieval (RAG)"]
        KB[(In-Memory Vector Index: 10 Runbooks<br/>gemini-embedding-001)]
        V_GATE{Similarity Score >= 0.65?}
        DEFLECT[Deflection Guardrail: No KB Match]
    end

    subgraph Inference ["3. Tiered Inference & Schema Validation"]
        LLM1[Primary Tier: Gemini 3.5 Flash-Lite + Enforced Schema]
        GATE1{Primary Call Succeeded?}
        LLM2[Fallback Tier: Gemini 3.8 Flash + Enforced Schema]
        GATE2{Fallback Call Succeeded?}
        FAIL[Unhandled Error Surfaces to Caller]
    end

    subgraph Egress ["4. Egress Validation & Resolution"]
        P_OUT[Pydantic Outbound Contract: TriageOutput]
        DISPATCH{Confidence >= 0.65 &<br/>Not Always-Escalate Category?}
        AUTO_ACTION[Autonomous Tool Dispatch: AUTOMATED_CRM - Mock]
        HITL[Human-in-the-Loop Review Queue]
        USER_SLA[SLA Notice: 2h High Priority / 24h Standard]
    end

    subgraph Observability ["5. Audit Telemetry & Offline Evals"]
        AUDIT[(Append-Only JSONL Audit Stream)]
        EVAL[Offline LLM-as-a-Judge Eval Harness<br/>Judge: OpenAI gpt-6.1-sol]
    end

    %% Workflow Connections
    USER --> P_IN
    P_IN -->|Schema Valid| CLEAN
    P_IN -->|Malformed Payload| IN_REJECT
    
    CLEAN --> KB
    KB --> V_GATE
    V_GATE -->|Grounded Context Found| LLM1
    V_GATE -->|No Relevant Context| DEFLECT
    
    LLM1 --> GATE1
    GATE1 -->|Success| P_OUT
    GATE1 -->|API Error Only| LLM2
    
    LLM2 --> GATE2
    GATE2 -->|Success| P_OUT
    GATE2 -->|Error - No Second Fallback| FAIL
    
    P_OUT --> DISPATCH
    DISPATCH -->|Yes| AUTO_ACTION
    DISPATCH -->|No| HITL
    DEFLECT --> HITL
    HITL --> USER_SLA
    
    %% Telemetry Logging Streams (Dotted lines)
    P_IN -.-> AUDIT
    V_GATE -.-> AUDIT
    GATE1 -.-> AUDIT
    GATE2 -.-> AUDIT
    P_OUT -.-> AUDIT
    HITL -.-> AUDIT
    AUDIT --> EVAL

    %% Styling
    classDef boundary fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef fallback fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef data fill:#ede7f6,stroke:#4527a0,stroke-width:2px;
    classDef success fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    class P_IN,V_GATE,GATE1,GATE2,DISPATCH boundary;
    class IN_REJECT,DEFLECT,LLM2,HITL,USER_SLA,FAIL fallback;
    class KB,AUDIT,EVAL data;
    class AUTO_ACTION,P_OUT success;
```

Key decisions:

- **Gate before generation.** The similarity gate runs *before* any generative call,
  so out-of-scope tickets cost an embedding, not a completion — and can't hallucinate
  a policy answer.
- **Cross-family eval.** Replies are judged by an OpenAI model (`gpt-6.1-sol`) against
  the Gemini generator, so the judge has no same-family leniency. Pass = overall 5/5
  only; a groundedness score of 1–2 caps the overall at 2. (`capstone/eval/`)
- **Config, not constants.** Model IDs and both 0.65 thresholds live in
  `capstone/config.py`, env-overridable — added after the original fallback model was
  retired mid-project (see Failure notes).

## Results so far (honest, small-n)

- Golden benchmark (10 cases: 3 schema violations, 2 deflections, 3 automations,
  2 escalations): **Schema compliance 100% (10/10), Routing accuracy 100% (10/10)** —
  re-run 2026-10-20 in a clean environment. 10 cases is a smoke test, not a
  benchmark; expanding to 50 is in progress.
- Telemetry on the committed log (149 events, 18 tickets, Sep 2026): triage
  p50 970 ms / p95 1,292 ms; retrieval p50 183 ms / p95 220 ms; routing
  63.6% human queue / 36.4% automated (n=33 executions).

## Run it (<5 minutes)

Requires Python 3.12 and a Gemini API key (an OpenAI key is only needed for the judge).

```bash
git clone https://github.com/stricklg/case-support-copilot.git
cd case-support-copilot
pip install -r requirements.txt
# create capstone/.env with:  GEMINI_API_KEY=...   (and OPENAI_API_KEY=... for eval)
cd capstone
streamlit run app.py        # the UI: submit a ticket, see routing + trace
python main.py              # runs the 10-case golden benchmark
python metrics.py           # latency / routing report from telemetry_events.jsonl
```

## Stack

Python 3.12 · google-genai · Pydantic v2 · NumPy (in-memory cosine index) ·
Streamlit · python-dotenv · OpenAI Responses API via stdlib `urllib` (judge only, no SDK)

## Layout

- `capstone/main.py` — pipeline (`run_pipeline`, `triage_and_categorize`), golden set, benchmark
- `capstone/context_engine.py` — KB embedding index + similarity gate
- `capstone/schemas.py` / `actions.py` — inbound contract / dispatch + SLA notices
- `capstone/config.py` — model IDs + thresholds
- `capstone/telemetry.py` / `metrics.py` — JSONL audit log / latency & routing reports
- `capstone/eval/` — LLM-as-judge harness (`judge.py`, `rubrics.py`)
- `capstone/kb/` — the 10 runbooks

## Limitations — read this before the code

- **The KB is 10 whole documents, embedded as single vectors — no chunking.**
  Longer knowledge base documents dilute: clearly-billing phrasings score 0.63–0.70 against the
  0.65 gate, so borderline tickets deflect that shouldn't. Chunking + threshold
  tuning is the known fix; it's eval work, not done yet.
- **`confidence` is not model confidence.** `triage_and_categorize()` overwrites it
  with the retrieval similarity score, so the dispatch gate is really gating on
  retrieval quality. Known conflation, kept visible rather than hidden; separating
  the two signals is planned.
- **The pipeline queries the KB twice per ticket** (once in `run_pipeline` for
  telemetry, again inside triage) — a duplicate embedding call per ticket. Also,
  the deflection branch in `run_pipeline` checks truthiness of a result object that
  is always truthy: dead code. Deflection actually happens inside triage.
- **Downstream is mocked.** The "CRM" and human queue are local functions, not
  integrations. The SLA notice is generated text, not a sent message.
- **No tests or CI yet.** The golden benchmark is the only executable check.

## Failure notes

- [The knowledge base that indexed 8 of 10 documents](docs/failure-kb-indexing.md) —
  an invisible Unicode character in two filenames, a 100% benchmark that couldn't
  see it, and the fix.
