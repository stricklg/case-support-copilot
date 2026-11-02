"""Judge result models: the pass bar and the strict-schema
shape the Responses API requires.

The rubric caps (e.g. groundedness 1-2 capping overall) are
instructions to the judge model inside rubrics.py, not code -
they are deliberately not tested here; what code owns is the
pass rule and the schema transform.
"""
import pytest
from pydantic import ValidationError

from judge import (CapstoneJudgeEval, TriageJudgeEval,
                   _strict_schema)


def reply(overall):
    return CapstoneJudgeEval(
        groundedness=3, accuracy=3, actionability=3, tone=3,
        overall=overall, explanation="x")


def test_pass_bar_is_overall_at_least_4():
    assert reply(4).passed is True
    assert reply(5).passed is True
    assert reply(3).passed is False


def test_scores_must_be_within_1_to_5():
    with pytest.raises(ValidationError):
        reply(6)
    with pytest.raises(ValidationError):
        reply(0)


def test_triage_pass_bar_matches():
    t = TriageJudgeEval(
        category_fit=5, priority_calibration=5,
        action_needed=5, issue_completeness=5, overall=3,
        explanation="x")
    assert t.passed is False


def test_strict_schema_requires_every_field():
    schema = _strict_schema(CapstoneJudgeEval)
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(
        schema["properties"].keys())
    assert all(set(spec) <= {"type", "description"}
               for spec in schema["properties"].values())
