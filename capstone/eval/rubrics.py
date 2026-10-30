"""Rubrics for the LLM-as-judge harness.

RUBRIC_PROJ_1/2/3 are extracted verbatim from llm_as_judge.ipynb
(2026-10-20) - they judged the Phase 1-3 coursework outputs and are
kept as historical artifacts. RUBRIC_CAPSTONE is the new rubric for
judging capstone draft replies (see judge.py).
"""

RUBRIC_PROJ_1 = """You are evaluating an AI system that analyzes application error logs, suggests root causes 
and remediation steps.

Assign a score from 1 to 5 based on these strict guidelines:

Score 5 (Excellent):
- Diagnostic Accuracy: Correctly identifies the exact root cause of the error log and provides error code.
- Remediation Quality: Provides accurate, practical, and safe steps to resolve the issue.
- Completeness: Covers necessary context (e.g., error codes, affected components) without hallucinating facts not present in the log.
- Clarity: The explanation is concise, technical, and easy for anyone to follow.

Score 3-4 (OK, but not acceptable):
- Diagnostic Accuracy: Identifies the general category or a plausible root cause, but misses minor technical nuances.
- Remediation Quality: Fix suggestions are correct but generic or missing specific implementation details.
- Minor Flaws: Contains minor fluff or slightly verbose explanations, but the core guidance remains sound.

Score 1-2 (Unsatisfactory / Failed):
- Misdiagnosis: Completely misidentifies the root cause of the error log.
- Dangerous or Incorrect Fixes: Suggests wrong, harmful, or hallucinated solutions that would not fix the bug.
- Severe Hallucination: Invents error codes, stack traces, or context not present in the input log.

PASS CRITERIA:
The response passes (passed=True) ONLY if the score is a 5."""

RUBRIC_PROJ_2 = """You are evaluating an AI system that processe and categorizes customer support 
tickets. It can only categorize tickets into the following primary categories: Billing, Shipping or Tech. Suggested
actions can only be "check_order_status" , "process_refund" or "manual_review.

Assign a score from 1 to 5 based on these strict guidelines:

Score 5 (Excellent):
- Categorization Accuracy: Correctly maps the ticket to the exact primary category (e.g., Billing, Technical Support, Account Access, Shipping).
- Urgency Assessment: Correctly assesses urgency (Low, Medium, High, Critical) matching the severity and tone of the customer request.
- Formatting: Strictly follows structured data rules without extra conversational text or hallucinated details.

Score 3-4 (OK, but doesn't pass):
- Off-by-One Urgency: Urgency rating is defensible but slightly conservative or aggressive (e.g., Medium instead of High).
- Category: Category is reasonable but selects a broader bucket than expected.

Score 1-2 (Unsatisfactory / Failed):
- Incorrect Categorization: Assigns ticket to a completely wrong domain (e.g., labeling a payment bug as Shipping).
- Severe Misjudging: Misclassifies high-urgency operational outages or security issues as Low urgency.

PASS CRITERIA:
The response passes (passed=True) ONLY if the score is 5."""

RUBRIC_PROJ_3 = """You are evaluating an AI RAG system that provides grounded support answers backed by retrieved 
Knowledge Base documents.

Assign a score from 1 to 5 based on these strict guidelines:

Score 5 (Excellent):
- Strict Groundedness: Every factual statement in the generated answer is directly supported by the provided KB Context.
- No Hallucinations: Does NOT make up policies, steps, or return windows not found in the context.
- Out-of-Scope Defense: Properly admits when the KB Context lacks sufficient information to answer the user's question.
- Citation Accuracy: Properly references source names/titles where applicable.

Score 3-4 (OK but doesn't pass):
- Mostly Grounded: Core answer is derived from KB context, but includes minor harmless filler or slight rephrasings.
- Missing Citation: Correct answer based on KB context, but omits citing the specific document name.

Score 1-2 (Unsatisfactory / Failed):
- Hallucination: Asserts facts, policies, or troubleshooting steps that DO NOT exist in the provided KB Context.
- Blind Answers: Answers unanswerable/out-of-scope queries as factual when the KB Context doesn't contain the answer.

PASS CRITERIA:
The response passes (passed=True) ONLY if the score is 5."""

RUBRIC_CAPSTONE = """
You are evaluating the draft customer reply produced by an AI support
triage system. The system retrieved one Knowledge Base runbook for the
ticket; the reply must be grounded in that runbook and nothing else.

Score EACH dimension from 1 to 5, then give an overall score:

1. Groundedness - every factual claim in the reply (steps, policies,
   timelines, limits) is directly supported by the KB context.
   Invented steps, policies, SLAs, or timelines are a severe failure,
   even if they sound plausible.
2. Accuracy - the reply addresses the actual issue in the ticket and
   the next steps it describes match what the runbook prescribes for
   this category of issue.
3. Actionability - the reply states clearly what happens next and
   what, if anything, is needed from the customer. Vague reassurance
   without a concrete next step scores low.
4. Tone - professional and empathetic, acknowledges the impact on the
   customer, concise, no blame, no internal jargon.

Band guidance:
Score 5 (Excellent): fully grounded, correct next steps from the
runbook, clear ask of the customer if one is needed, tone is right.
Score 3-4 (OK): core content is grounded and
correct, but has a real flaw - a missing next step, a needed customer
action left unstated, minor unsupported filler, or tone that is flat
or overly verbose.
Score 1-2 (Unsatisfactory / Failed): any hallucinated policy, step, or
timeline; next steps contradict the runbook; the reply answers a
different problem than the ticket raised; or it promises an outcome
the runbook does not support.

PASS CRITERIA:
The reply passes (passed=True) if the overall score is 4 or 5.
A groundedness score of 1 or 2 caps the overall score at 2,
regardless of the other dimensions.
"""


RUBRIC_TRIAGE = """
You are evaluating the triage decision produced by an AI support
triage system. The system read one customer ticket and produced a
structured triage: a primary category, a priority, an action_needed
flag, and a list of any additional distinct issues in the ticket
(secondary_categories). Judge the triage decision against the
ticket and the category definitions - NOT against the reply text.

Score EACH dimension from 1 to 5, then give an overall score:

1. Category fit - the primary category is the best fit for the
   ticket's main issue under the category definitions.
2. Priority calibration - the priority matches the severity and
   business impact described in the ticket, per the priority
   guidelines in the category definitions.
3. Action-needed correctness - action_needed is true when the
   ticket reports an active error or requests an account change,
   and false when the message is an acknowledgment, informational,
   or an automated notice.
4. Issue completeness - every distinct support issue in the ticket
   is captured (primary category plus secondary_categories), and
   nothing else is listed. Symptoms, consequences, error details,
   and background events are not distinct issues.

Band guidance:
Score 5 (Excellent): primary category is the exact best fit,
priority matches the ticket's impact, action_needed is correct,
and the issue list is complete with no phantom issues.
Score 3-4 (OK; a 4 passes, a 3 does not): the primary category is
a defensible broader or adjacent bucket, OR the priority is off
by one level in a defensible direction, OR a minor issue is
missed or a borderline item is listed as a second issue.
Score 1-2 (Unsatisfactory / Failed): the primary category is the
wrong domain; a high-impact outage, lockout, or security issue
is scored low priority; action_needed is backwards; or a genuine
second issue is missed entirely.

PASS CRITERIA:
The triage passes (passed=True) if the overall score is 4 or 5.
A wrong primary category caps the overall score at 2, regardless
of the other dimensions.
"""
