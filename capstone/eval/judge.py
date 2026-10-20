"""LLM-as-judge for the capstone, extracted from llm_as_judge.ipynb.

The judge is OpenAI (config.JUDGE_MODEL) while the system under test
generates with Gemini - cross-family judging, so the judge has no
same-family leniency toward the generator. Calls use stdlib urllib
direct REST, the same pattern as the Kestra flows; no OpenAI SDK.

The notebook original judged with Gemini and a single holistic score.
This module keeps its prompt structure and strict pass rule, fixes
its field-name typos (explination -> explanation), and returns
per-dimension scores so failures are diagnosable.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# The capstone package is the parent folder; its config.py owns the
# model names and its .env owns the API keys (gitignored).
CAPSTONE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAPSTONE_DIR))
load_dotenv(CAPSTONE_DIR / ".env")

from config import JUDGE_MODEL  # noqa: E402

OPENAI_URL = "https://api.openai.com/v1/responses"


class JudgeEval(BaseModel):
    """Original notebook schema, typo fixed. Single holistic score."""

    score: int = Field(ge=1, le=5)
    explanation: str

    @property
    def passed(self) -> bool:
        return self.score == 5


class CapstoneJudgeEval(BaseModel):
    """Per-dimension scores for a capstone draft reply."""

    groundedness: int = Field(ge=1, le=5)
    accuracy: int = Field(ge=1, le=5)
    actionability: int = Field(ge=1, le=5)
    tone: int = Field(ge=1, le=5)
    overall: int = Field(ge=1, le=5)
    explanation: str

    @property
    def passed(self) -> bool:
        # The notebook strict rule: pass only at a perfect score.
        return self.overall == 5


def _strict_schema(model: type[BaseModel]) -> dict:
    """JSON schema in the strict form the Responses API requires."""
    raw = model.model_json_schema()
    props = {}
    for name, spec in raw["properties"].items():
        clean = {"type": spec["type"]}
        if "description" in spec:
            clean["description"] = spec["description"]
        props[name] = clean
    return {
        "type": "object",
        "properties": props,
        "required": list(props.keys()),
        "additionalProperties": False,
    }


def _call_judge(prompt: str, model_schema: type[BaseModel]) -> BaseModel:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not found in capstone/.env")
    body = {
        "model": JUDGE_MODEL,
        "input": prompt,
        "reasoning": {"effort": "low"},
        "max_output_tokens": 900,
        "text": {
            "format": {
                "type": "json_schema",
                "name": model_schema.__name__,
                "strict": True,
                "schema": _strict_schema(model_schema),
            }
        },
    }
    req = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:300]
        raise RuntimeError(f"Judge API error {e.code}: {detail}") from e
    text = ""
    for item in data.get("output", []):
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                text += part.get("text", "")
    if not text:
        raise RuntimeError("Judge returned no output text")
    return model_schema.model_validate_json(text)


def build_judge_prompt(
    user_input: str,
    generated_output: str,
    rubric: str,
    expected_ground_truth: Optional[str] = None,
    kb_context: Optional[str] = None,
) -> str:
    """Same prompt structure as the notebook evaluate_with_judge()."""
    return f"""You are an impartial, highly critical AI evaluation judge.
Your task is to evaluate an LLM generated response for quality and
correctness against a provided rubric.

== Evaluation Rubric ==
{rubric}

== User Input ==
{user_input}

=== KNOWLEDGE BASE CONTEXT (Retrieved Reference Documents) ===
{kb_context if kb_context else "Not Applicable"}

== Expected Grounded Truth if applicable ==
{expected_ground_truth if expected_ground_truth else "Not Applicable"}

== System Generated Output ==
{generated_output}

Evaluate the output objectively against the rubric.
"""


def evaluate_with_judge(
    user_input: str,
    generated_output: str,
    rubric: str,
    expected_ground_truth: Optional[str] = None,
    kb_context: Optional[str] = None,
) -> JudgeEval:
    """Notebook-compatible entry point: one holistic score."""
    prompt = build_judge_prompt(
        user_input, generated_output, rubric,
        expected_ground_truth, kb_context,
    )
    return _call_judge(prompt, JudgeEval)


def evaluate_capstone_reply(
    ticket_text: str,
    draft_reply: str,
    rubric: str,
    kb_context: Optional[str] = None,
    expected_ground_truth: Optional[str] = None,
) -> CapstoneJudgeEval:
    """Judge one capstone draft reply, per-dimension scores."""
    prompt = build_judge_prompt(
        ticket_text, draft_reply, rubric,
        expected_ground_truth, kb_context,
    )
    return _call_judge(prompt, CapstoneJudgeEval)
