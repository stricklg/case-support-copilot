#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pydantic import BaseModel, Field, ValidationError
from enum import Enum
from google import genai
from google.genai import types, errors
from typing import List, Optional, Any, Dict, Tuple
from dotenv import load_dotenv
from pathlib import Path
import time
from context_engine import KB
from schemas import InboundTicket
from telemetry import TelemetryEvent, log_event, LOG_FILE_PATH
from actions import ExecutionResult, dispatch_action
from types import SimpleNamespace
from config import PRIMARY_MODEL, FALLBACK_MODEL, EMBEDDING_MODEL, SIMILARITY_THRESHOLD
import os
import json

load_dotenv()


# In[2]:


if __name__ == "__main__":
  kb_dir = Path.cwd() / "kb"
  kb = KB(
      kb_dir=kb_dir,
      similarity_threshold=SIMILARITY_THRESHOLD,
      model=EMBEDDING_MODEL,
  )
  kb.build_index()


# In[3]:


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Category(str, Enum):
    INTEGRATION_WEBHOOK_FAILURE = "integration webhook failure"
    BILLING_SUBSCRIPTION_ISSUE = "billing subscription issue"
    QUOTA_RATE_LIMIT_EXCEEDED = "quota/rate limit exceeded"
    AUTH_SSO_PROVISIONING = "auth/sso provisioning"
    WORKFLOW_SYNTAX_EXECUTION_ERROR = "workflow syntax/execution error"
    PERFORMANCE_LATENCY_ISSUE = "performance/latency issue"
    DATA_EXPORT_COMPLIANCE = "data export compliance"
    FEATURE_REQUEST = "feature request"
    USER_SEAT_MANAGEMENT = "user/seat management"
    ONBOARDING_ENVIRONMENT_SETUP = "onboarding/environment setup"
    OTHER = "other"

class TriageOutput(BaseModel):
    category: Category 
    priority: Priority
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0, le=1.0,
        description=("The triage model's own confidence in its "
          "categorization, 0.0 to 1.0. This is the only confidence "
          "the dispatch gate reads."),
    )
    retrieval_similarity: Optional[float] = Field(
        default=None,
        ge=0.0, le=1.0,
        description=("Retrieval similarity of the matched runbook, "
          "set by the pipeline after the model call. Never used as "
          "model confidence."),
    )
    retrieval_margin: Optional[float] = Field(
        default=None,
        description=("Margin between the winning runbook's best "
          "chunk score and the best chunk from any other runbook, "
          "set by the pipeline after the model call. The dispatch "
          "margin floor reads it; it is never model confidence."),
    )
    secondary_categories: List[Category] = Field(
        default_factory=list,
        description=("Other distinct support issues raised in "
          "the same ticket, beyond the primary category. A "
          "distinct issue is a separate problem that would need "
          "its own handling; symptoms, consequences, error "
          "details, and background events are not separate "
          "issues. List an issue only when the customer is "
          "reporting a problem with it or requesting action "
          "on it; a fact mentioned in passing is not an issue. "
          "Empty when the ticket raises one issue."),
    )
    action_needed: bool = Field(
        description=("True if the ticket requires operational handling, troubleshooting, "
          "or system changes (e.g., webhook failure, quota reset, billing adjustment). "
          "False if the message is purely informational, an acknowledgment,confirmation of a fix, or out-of-office automated reply."
          )
    )
    draft_reply: str = Field(
        description="A professional, concise customer-facing reply acknowledging the"
          " issue and outlining immediate next steps."
    )


# In[4]:


def run_pipeline(
    raw_payload: Dict[str, Any], kb: KB
) -> Tuple[int, Dict[str, Any]]:
    ticket_id = raw_payload.get("ticket_id", "UNKNOWN_ID")
    total_start = time.perf_counter()

    # Ingestion Boundary
    t0 = time.perf_counter()
    status_code, result = ingest_ticket(raw_payload)
    ingest_ms = (time.perf_counter() - t0) * 1000

    if status_code !=200:
        log_event(
            TelemetryEvent(
                ticket_id=ticket_id,
                stage="INGESTION",
                status="REJECTION",
                latency_ms=ingest_ms,
                details=result,
            )
        )
        return status_code, result


    ticket: InboundTicket = result
    log_event(
        TelemetryEvent(
            ticket_id=ticket.ticket_id,
            stage="INGESTION",
            status="SUCCESS",
            latency_ms=ingest_ms,
            details={"customer_email": ticket.customer_email},
        )
    )

    #2 Retrieval Boundary
    t0 = time.perf_counter()
    query_text = ticket.composite_text
    retrieval_match = kb.query(query_text)
    retrieval_ms = (time.perf_counter() - t0) * 1000

    if not retrieval_match:
        log_event(
            TelemetryEvent(
                ticket_id=ticket.ticket_id,
                stage="RETRIEVAL",
                status="DEFLECTED",
                latency_ms=retrieval_ms,
                details={"reason": "Below similiarity gate"},
            )
        )
        # Deflection path: Mock fallback output for routing
        triage_output = SimpleNamespace(
            category="other", confidence=0.0, priority="normal"
        )
    else:
        log_event(
            TelemetryEvent(
                ticket_id=ticket.ticket_id,
                stage="RETRIEVAL",
                status="SUCCESS",
                latency_ms=retrieval_ms,
                details={
                    "doc_name": retrieval_match.matched_kb,
                    "score": retrieval_match.similarity_score,
                },
            )
        )

        # 3 Triage Inference Boundary
        t0 = time.perf_counter()
        triage_output = triage_and_categorize(query_text, kb)
        triage_ms = (time.perf_counter() - t0) *1000

        log_event(
            TelemetryEvent(
                ticket_id=ticket.ticket_id,
                stage="TRIAGE",
                status="SUCCESS",
                latency_ms=triage_ms,
                details={
                    "category": getattr(triage_output.category, "value", str(triage_output.category)
                    ),
                    "confidence": triage_output.confidence,
                },
            )
        )

        # 4 Downstream Execution Boundary
        t0 = time.perf_counter()
        exec_result: ExecutionResult = dispatch_action(ticket, triage_output)
        exec_ms = (time.perf_counter() - t0) * 1000

        log_event(
            TelemetryEvent(
                ticket_id=ticket.ticket_id,
                stage="EXECUTION",
                status="SUCCESS",
                latency_ms=exec_ms,
                details={
                    "destination": exec_result.destination.value,
                    "has_sla_notice": exec_result.sla_notice is not None,
                },
            )
        )

        total_ms = (time.perf_counter() - total_start) * 1000
        return 200, {
            "ticket": ticket.model_dump(),
            "triage": {
                "category": getattr(
                    triage_output.category, "value",
                    str(triage_output.category),
                ),
                "priority": getattr(
                    triage_output.priority, "value",
                    str(triage_output.priority),
                ),
                "confidence": triage_output.confidence,
                "retrieval_similarity":
                    triage_output.retrieval_similarity,
                "retrieval_margin":
                    triage_output.retrieval_margin,
                "action_needed":
                    getattr(triage_output, "action_needed", None),
                "secondary_categories": [
                    getattr(c, "value", str(c))
                    for c in (
                        getattr(
                            triage_output,
                            "secondary_categories", None) or []
                    )
                ],
                "draft_reply": triage_output.draft_reply,
            },
            "retrieval": {
                "matched_kb": retrieval_match.matched_kb,
                "similarity_score": retrieval_match.similarity_score,
                "is_deflected": retrieval_match.is_deflected,
                "matched_content": retrieval_match.matched_content,
            },
            "execution": exec_result.model_dump(),
            "total_latency_ms": total_ms,
        }


# In[5]:


prompt_file = Path(__file__).resolve().parent /"system_triage_instructions.md"
system_prompt_text = prompt_file.read_text(encoding="utf-8")

client = genai.Client()  

def triage_and_categorize(ticket_text: str, kb) -> TriageOutput:
    retrieval = kb.query(ticket_text)

    if retrieval.is_deflected:
        print(
            f"[DEFLECTION] Similarity {retrieval.similarity_score:.3f}< {kb.threshold}"
        )
        return TriageOutput(
            category=Category.OTHER,
            priority=Priority.LOW,
            confidence=0.0,
            retrieval_similarity=round(
                retrieval.similarity_score, 3),
            retrieval_margin=round(retrieval.margin, 3),
            action_needed=True,
            draft_reply=(
                "Thank you for reaching out to OmniFlow support. Your inquiry "
                "requires further evaluation. A support engineer will reach out to"
                "you soon."   
            ),
        )
    print(f"[MATCH FOUND] Matched {retrieval.matched_kb} (Score: {retrieval.similarity_score:.3f})")

    augmented_prompt = f"""### OPERATIONAL KB CONTEXT
    File: {retrieval.matched_kb}
    Content: {retrieval.matched_content}

    ### INCOMING CUSTOMER TICKET
    {ticket_text}
    """
    config=types.GenerateContentConfig(
            system_instruction = system_prompt_text,
                    response_mime_type = "application/json",
                    response_schema = TriageOutput,
                    temperature = 0.0,
            )

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents= augmented_prompt,
            config=config,
        )

    except (errors.APIError, Exception) as e:
        print(f"{PRIMARY_MODEL} Failed with error: {e}. Falling back to {FALLBACK_MODEL}.")
        response = client.models.generate_content(
            model = FALLBACK_MODEL,
            contents = augmented_prompt,
            config=config,
        )

    result: TriageOutput = (response.parsed or TriageOutput.model_validate_json(response.text))
    # Keep the two signals separate: the model's confidence stays
    # the model's (the dispatch gate reads it), and the retrieval
    # similarity is recorded on its own field. Until 2026-10-27
    # this line overwrote confidence with the similarity, so the
    # dispatch gate re-judged retrieval instead of triage quality.
    result.retrieval_similarity = round(
        retrieval.similarity_score, 3)
    result.retrieval_margin = round(retrieval.margin, 3)
    if result.confidence is None:
        # No self-reported confidence: route conservatively.
        result.confidence = 0.0
    return result



# In[6]:


def ingest_ticket(raw_payload: Dict[str, Any]) -> Tuple[int, Any]:
    """Injest and validates raw tickets.
    Returns:
        (200, InboundTicket) on success
        (400, dict) on malformed/invalid input
    """
    try:
        ticket = InboundTicket(**raw_payload)
        return 200, ticket
    except ValidationError as exec:
        # Format readable error messages for API consumers
        error_details = [
            {
                "field": "-> ".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exec.errors()
        ]
        return 400, {"status": "Bad Request", "errors": error_details}


# In[7]:


def process_inbound_ticket(raw_payload: dict, kb: KB):
    """End-to-end handler: Ingests, validates, retrieves context, and triages."""
    status, result = ingest_ticket(raw_payload)

    if status != 200:
        print(f"[REJECTED {status} Malformed payload halting pipeline.]")
        return status, result

    ticket: InboundTicket = result
    print(f"[ACCEPTED 200] Processing ticket {ticket.ticket_id}...")

    triage_result = triage_and_categorize(ticket.composite_text, kb)
    return 200, triage_result


# In[8]:


GOLDEN_EVAL_SET = [
    # Schema Violations (Expected: 400 Bad Request)
    {
        "id": "G01",
        "exp_status": 400,
        "exp_dest": None,
        "payload": {
            "ticket_id": "G01",
            "customer_email": "bad",
            "subject": "Hi",
            "body": "Short",
        },
    },
    {
        "id": "G02",
        "exp_status": 400,
        "exp_dest": None,
        "payload": {
            "ticket_id": "G02",
            "customer_email": "a@b.com",
            "subject": "   ",
            "body": "Valid body text here.",
        },
    },
    {
        "id": "G03",
        "exp_status": 400,
        "exp_dest": None,
        "payload": {
            "ticket_id": "G03",
            "customer_email": "a@b.com",
            "subject": "Missing body",
        },
    },
    # Deflections / Out of Scope (Expected: 200, HITL_QUEUE, Category: other)
    {
        "id": "G04",
        "exp_status": 200,
        "exp_dest": "HITL_QUEUE",
        "payload": {
            "ticket_id": "G04",
            "customer_email": "ops@co.com",
            "subject": "Lunch order",
            "body": "What are we ordering for the company lunch downtown?",
        },
    },
    {
        "id": "G05",
        "exp_status": 200,
        "exp_dest": "HITL_QUEUE",
        "payload": {
            "ticket_id": "G05",
            "customer_email": "ops@co.com",
            "subject": "Weather check",
            "body": "Is it going to snow this afternoon?",
        },
    },
    # In-Scope Automations (Expected: 200, AUTOMATED_CRM)
    {
        "id": "G06",
        "exp_status": 200,
        "exp_dest": "AUTOMATED_CRM",
        "payload": {
            "ticket_id": "G06",
            "customer_email": "dev@co.com",
            "subject": "HubSpot webhook 500 error",
            "body": (
                "Our webhook receiver is returning 500 internal server error on"
                " contact create events."
            ),
        },
    },
    {
        "id": "G07",
        "exp_status": 200,
        "exp_dest": "AUTOMATED_CRM",
        "payload": {
            "ticket_id": "G07",
            "customer_email": "api@co.com",
            "subject": "API 429 rate limits",
            "body": (
                "We hit 429 rate limits on our batch sync endpoint during our"
                " nightly sync run."
            ),
        },
    },
    {
        "id": "G08",
        "exp_status": 200,
        "exp_dest": "AUTOMATED_CRM",
        "payload": {
            "ticket_id": "G08",
            "customer_email": "billing@co.com",
            "subject": "License expansion",
            "body": (
                "Need to purchase 20 additional user seats for our engineering"
                " workspace."
            ),
        },
    },
    # In-Scope Escalations (Expected: 200, HITL_QUEUE with SLA notice)
    {
        "id": "G09",
        "exp_status": 200,
        "exp_dest": "HITL_QUEUE",
        "payload": {
            "ticket_id": "G09",
            "customer_email": "user@co.com",
            "subject": "SSO login configuration",
            "body": (
                "Need help setting up Okta SAML assertions for our new"
                " subdomain."
            ),
        },
    },
    {
        "id": "G10",
        "exp_status": 200,
        "exp_dest": "HITL_QUEUE",
        "payload": {
            "ticket_id": "G10",
            "customer_email": "data@co.com",
            "subject": "Custom export request",
            "body": (
                "Can you add parquet export support for raw audit log tables?"
            ),
        },
    },
]


def run_benchmark(kb: KB):
  print(f"\nRunning Golden Dataset Evaluation ({len(GOLDEN_EVAL_SET)} cases)...")
  schema_passes = 0
  routing_passes = 0

  for case in GOLDEN_EVAL_SET:
    status, res = run_pipeline(case["payload"], kb)

    # 1. Validate HTTP status compliance
    if status == case["exp_status"]:
      schema_passes += 1

    # 2. Validate downstream destination
    if status == 200:
      actual_dest = str(res["execution"]["destination"])
      # Handles both Enum objects and raw string values
      if hasattr(res["execution"]["destination"], "value"):
        actual_dest = res["execution"]["destination"].value

      if actual_dest == case["exp_dest"]:
        routing_passes += 1
    elif status == 400:
      # Blocked payloads never reach routing
      routing_passes += 1

  total = len(GOLDEN_EVAL_SET)
  print("\n" + "=" * 45)
  print("       PIPELINE BENCHMARK SUMMARY            ")
  print("=" * 45)
  print(
      f" Schema Compliance:  {schema_passes / total * 100:.1f}% "
      f" ({schema_passes}/{total})"
  )
  print(
      f" Routing Accuracy:   {routing_passes / total * 100:.1f}% "
      f" ({routing_passes}/{total})"
  )
  print("=" * 45 + "\n")


if __name__ == "__main__":
  run_benchmark(kb)


