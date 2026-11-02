"""Inbound ticket validation (schemas.InboundTicket).

These rejections are what the eval's status-400 cases
exercise end-to-end; here they are pinned at the seam.
"""
import pytest
from pydantic import ValidationError

from schemas import InboundTicket


def payload(**over):
    base = {
        "ticket_id": "T-100",
        "customer_email": "user@example.com",
        "subject": "Webhook failing",
        "body": "Our webhooks return 500 errors since Tuesday.",
    }
    base.update(over)
    return base


def test_valid_ticket_and_composite_text():
    t = InboundTicket(**payload())
    assert t.composite_text == (
        "Subject: Webhook failing\n"
        "Body: Our webhooks return 500 errors since Tuesday.")


def test_whitespace_is_normalised():
    t = InboundTicket(**payload(subject="  Webhook   failing  "))
    assert t.subject == "Webhook failing"


@pytest.mark.parametrize("over", [
    {"ticket_id": "ab"},
    {"customer_email": "not-an-email"},
    {"customer_email": "missing@tld"},
    {"subject": "ab"},
    {"subject": "   "},
    {"body": "too short"},
    {"subject": 42},
])
def test_invalid_tickets_are_rejected(over):
    with pytest.raises(ValidationError):
        InboundTicket(**payload(**over))
