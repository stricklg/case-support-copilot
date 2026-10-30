from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from schemas import InboundTicket
from config import CONFIDENCE_THRESHOLD, MARGIN_FLOOR

class RoutingDesignation(str, Enum):
    AUTOMATED_CRM = "AUTOMATED_CRM"
    HITL_QUEUE = "HITL_QUEUE"

class ExecutionResult(BaseModel):
    """Structured results of downstream dispatch."""

    ticket_id: str
    destination: RoutingDesignation
    confidence: float
    action_summary: str
    sla_notice: Optional[str] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

def format_sla_notice(priority: str, category: str) -> str:
    """Generates a user-facing SLA response based on priority."""
    now = datetime.now(timezone.utc)

    if priority.lower() in ["urgent", "critical", "high"]:
        sla_delta = timedelta(hours=2)
        tier = "Priority Escalation"
    else:
        sla_delta = timedelta(hours=24)
        tier = "Standard Review"

    target_time = (now + sla_delta).strftime("%Y-%m-%d %H:%M UTC")

    return (
        f"Thank you for contacting support. Your requestion regarding '{category}' "
        f"has been escalated to our specialist team under {tier} tier."
        f"An engineer will review your ticket and respond before {target_time}."
    )

def sync_to_mock_crm(
        ticket: InboundTicket, triage_output: Any
) -> Dict[str, Any]:
    """Mock CRM function."""
    category = getattr(
        triage_output.category, "value", str(triage_output.category)
    )
    print(f"[CRM DISPATCh] Auto-routed ticket {ticket.ticket_id} to {category}.")
    return {
        "crm_record_id": f"CRM-{ticket.ticket_id}",
        "status": "AUTO_ASSIGNED",
        "assigned_to": f"team-{category.replace(' ', '-')}-tier1",
    }

def route_to_hitl_queue(
        ticket: InboundTicket, triage_output: Any, reason: str
) -> Dict[str, Any]:
    """Mock Human-in-the-loop triage queue."""
    print(f"[HITL QUEUE] Flagged {ticket.ticket_id} for review. Reason: {reason}")
    return {
        "queue_id": f"HITL-{ticket.ticket_id}",
        "status": "PENDING_HUMAN_REVIEW",
        "flag_reason": reason,
    }

def dispatch_action(ticket: InboundTicket, triage_output: Any) -> ExecutionResult:
    """Phase 4 Dispatcher:
    
    Routes >= 0.65 to CRM automation, < 0.65 to HITL review with user-facing SLA.
    """
    confidence = float(triage_output.confidence)
    category = getattr(
        triage_output.category, "value", str(triage_output.category)
    ).lower()
    priority = getattr(triage_output, "priority", "normal")
    # Categories that always require human review. These strings must
    # match the Category enum values in main.py exactly: the previous
    # labels ("sso configuration", "custom export", "security
    # compliance") matched no enum value, so the SSO and data-export
    # escalations never fired and routing fell to the confidence
    # number alone.
    ESCALATION_CATEGORIES = {
        "feature request",
        "auth/sso provisioning",
        "data export compliance",
        "other",
    }
    is_escalation = category.lower() in ESCALATION_CATEGORIES

    # Margin Gate: a contested runbook match (the winner barely
    # beat another runbook's best chunk) goes to human review no
    # matter what the model reports about its own confidence.
    # Measured 2026-10-27: every category error in the golden set
    # sat in the bottom of the margin distribution while carrying
    # self-reported confidence 0.95.
    margin = getattr(triage_output, "retrieval_margin", None)
    margin_contested = (
        margin is not None and margin < MARGIN_FLOOR
    )

    # Multi-Issue Gate: a ticket raising a second distinct issue
    # goes to human review - automated handling resolves the
    # primary category only, so the second issue would be closed
    # unhandled. Geoff's rule, 2026-10-27 (golden case G46).
    secondary = getattr(
        triage_output, "secondary_categories", None) or []
    secondary_labels = [
        getattr(c, "value", str(c)) for c in secondary
    ]
    is_multi_issue = len(secondary_labels) > 0

    # Confidence Gate: >= .65 and not an automatic escalation category-> Automated CRM
    if (
        confidence >= CONFIDENCE_THRESHOLD
        and not is_escalation
        and not margin_contested
        and not is_multi_issue
    ):
        crm_res = sync_to_mock_crm(ticket, triage_output)
        return ExecutionResult(
            ticket_id=ticket.ticket_id,
            destination=RoutingDesignation.AUTOMATED_CRM,
            confidence=confidence,
            action_summary=f"Automated resolution triggered: {crm_res['crm_record_id']}",
            sla_notice=None,
        )

    # Low Confidence / Ambiguous / Other -> HITL Queue with user SLA
    if category.lower() == "other":
        reason = "Classified as out-of-scope/other"
    elif is_escalation:
        reason = (
            f"Escalation category ({category}) requires human review"
        )
    elif is_multi_issue:
        reason = (
            "Multiple distinct issues in one ticket (also: "
            f"{', '.join(secondary_labels)}) require human review"
        )
    elif margin_contested:
        reason = (
            f"Ambiguous runbook match (margin {margin:.3f} "
            f"< {MARGIN_FLOOR}) requires human review"
        )
    else:
        reason = (
            f"Low confidence ({confidence:.2f} < {CONFIDENCE_THRESHOLD})"
        )

    hitl_res = route_to_hitl_queue(ticket, triage_output, reason=reason)
    sla_text = format_sla_notice(priority=priority, category=category)

    return ExecutionResult(
        ticket_id=ticket.ticket_id,
        destination=RoutingDesignation.HITL_QUEUE,
        confidence=confidence,
        action_summary=f"Routed to HITL queue ({hitl_res['queue_id']}): {reason}",
        sla_notice=sla_text,
    )