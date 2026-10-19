from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from schemas import InboundTicket

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

CONFIDENCE_THRESHOLD = 0.65

def dispatch_action(ticket: InboundTicket, triage_output: Any) -> ExecutionResult:
    """Phase 4 Dispatcher:
    
    Routes >= 0.65 to CRM automation, < 0.65 to HITL review with user-facing SLA.
    """
    confidence = float(triage_output.confidence)
    category = getattr(
        triage_output.category, "value", str(triage_output.category)
    ).lower()
    priority = getattr(triage_output, "priority", "normal")
    #Categories that always require human review
    ESCALATION_CATEGORIES = {
        "feature request",
        "custom export",
        "sso configuration",
        "security compliance",
        "other",
    }

    # Confidence Gate: >= .65 and not an automatic escalation category-> Automated CRM
    if (
        confidence >= CONFIDENCE_THRESHOLD and category.lower() not in ESCALATION_CATEGORIES
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
    reason = (
        f"Low confidence ({confidence:.2f} < {CONFIDENCE_THRESHOLD})"
        if category.lower() != "other"
        else "Classified as out-of-scope/other"
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