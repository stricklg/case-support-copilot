# OmniFlow Runbook: Workflow Syntax & Execution Errors

**Category:** `workflow_syntax_execution_error`  
**Applies to:** Branch nodes, JSON schema validation, transform expressions, regex steps

## Common Syntax Failures & Diagnostics
1. **JSON Schema Validation Failure (`ERR_PAYLOAD_SCHEMA_MISMATCH`):**
   - Occurs when payload fields fail strict typing (e.g., received string `"120"` where integer `120` was expected).
   - Instruct the customer to test payload validation under **Workflow Builder > Run History > Node Inspector > Raw Input**.
   - Recommend adding a **Sanitize / Coerce Node** prior to branch evaluation.

2. **Regex Evaluation Timeouts (`ERR_REGEX_TIMEOUT`):**
   - Workflows throttle execution if a custom regex step exceeds 500ms (catastrophic backtracking protection).
   - Guide the customer to optimize pattern anchors (`^` and `$`) and replace nested quantifiers.

3. **Infinite Loop Detection:**
   - Workflows with circular parent-child triggers automatically suspend after 25 recursive executions.
   - Advise the customer to verify recursion guards or toggle **Idempotency Deduplication Key** under Step Settings.

## Escalation Criteria
- If valid customer workflows throw unhandled `502 Bad Gateway` runtime errors during node processing, escalate to `@engine-runtime` with priority `HIGH`.
