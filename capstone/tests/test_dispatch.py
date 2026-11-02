"""Dispatch gate tests (actions.dispatch_action).

The dispatcher is duck-typed, so a SimpleNamespace stands in
for TriageOutput - the same way the October 2026 proving case
exercised it before pytest existed. The escalation-category
parametrization is the regression test for the dead-label
bug: every Category value is driven through the gate, so a
label that matches nothing fails loudly here.
"""
from types import SimpleNamespace

import pytest

from actions import RoutingDesignation, dispatch_action
from config import CONFIDENCE_THRESHOLD, MARGIN_FLOOR
from main import Category
from schemas import InboundTicket

ESCALATION = ["feature request", "auth/sso provisioning",
              "data export compliance", "other"]
AUTOMATABLE = [c.value for c in Category
               if c.value not in ESCALATION]


def ticket():
    return InboundTicket(
        ticket_id="T-100",
        customer_email="user@example.com",
        subject="Webhook failing",
        body="Our webhooks return 500 errors since Tuesday.",
    )


def triage(category, confidence=0.99, margin=0.20,
           secondary=None, priority="low"):
    return SimpleNamespace(
        category=category, confidence=confidence,
        priority=priority, retrieval_margin=margin,
        secondary_categories=secondary or [])


def by_value(value):
    return next(c for c in Category if c.value == value)


@pytest.mark.parametrize("value", ESCALATION)
def test_escalation_categories_always_queue(value):
    res = dispatch_action(
        ticket(), triage(by_value(value), confidence=0.99))
    assert res.destination is RoutingDesignation.HITL_QUEUE


@pytest.mark.parametrize("value", AUTOMATABLE)
def test_clean_high_confidence_automates(value):
    res = dispatch_action(
        ticket(), triage(by_value(value), confidence=0.99))
    assert res.destination is RoutingDesignation.AUTOMATED_CRM
    assert res.sla_notice is None


def test_confidence_boundary():
    cat = by_value("integration webhook failure")
    at = dispatch_action(
        ticket(), triage(cat, confidence=CONFIDENCE_THRESHOLD))
    assert at.destination is RoutingDesignation.AUTOMATED_CRM
    below = dispatch_action(
        ticket(),
        triage(cat, confidence=CONFIDENCE_THRESHOLD - 0.01))
    assert below.destination is RoutingDesignation.HITL_QUEUE
    assert "Low confidence" in below.action_summary


def test_margin_gate():
    cat = by_value("billing subscription issue")
    contested = dispatch_action(
        ticket(), triage(cat, margin=MARGIN_FLOOR - 0.001))
    assert contested.destination is RoutingDesignation.HITL_QUEUE
    assert "Ambiguous runbook match" in contested.action_summary
    clear = dispatch_action(
        ticket(), triage(cat, margin=MARGIN_FLOOR))
    assert clear.destination is RoutingDesignation.AUTOMATED_CRM
    unknown = dispatch_action(ticket(), triage(cat, margin=None))
    assert unknown.destination is RoutingDesignation.AUTOMATED_CRM


def test_multi_issue_gate_and_reason():
    cat = by_value("integration webhook failure")
    second = by_value("billing subscription issue")
    res = dispatch_action(ticket(), triage(cat, secondary=[second]))
    assert res.destination is RoutingDesignation.HITL_QUEUE
    assert "Multiple distinct issues" in res.action_summary
    assert "billing subscription issue" in res.action_summary


def test_escalation_reason_beats_multi_issue():
    cat = by_value("feature request")
    second = by_value("billing subscription issue")
    res = dispatch_action(ticket(), triage(cat, secondary=[second]))
    assert "Escalation category" in res.action_summary


def test_other_reason_wording():
    res = dispatch_action(ticket(), triage(by_value("other")))
    assert "out-of-scope/other" in res.action_summary


def test_hitl_sla_tiers():
    cat = by_value("integration webhook failure")
    high = dispatch_action(
        ticket(), triage(cat, confidence=0.5, priority="high"))
    assert "Priority Escalation" in high.sla_notice
    low = dispatch_action(
        ticket(), triage(cat, confidence=0.5, priority="low"))
    assert "Standard Review" in low.sla_notice
