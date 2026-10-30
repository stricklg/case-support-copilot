# Capstone eval report

Run at: 2026-10-30T15:51:26.929354+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 84.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 3.48
- Avg accuracy: 3.52
- Avg actionability: 3.58
- Avg tone: 3.85
- Avg overall: 2.91
- Pass rate (overall = 5): 0.03
- Pass rate (overall >= 4): 0.303

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly follows the HTTP 500/504 guidance: check the status page for ingestion pipeline delays and explain the exact retry intervals if delivery is delayed more than 15 minutes. However, 'We are monitoring this issue for you' asserts an ongoing support action that is not supported by the runbook or evidence provided. This is unsupported reassurance rather than an invented remediation policy or timeline, but it prevents full groundedness. The status-page check is a concrete customer action, though the reply does not clarify what happens if no delay is reported or the error persists. The tone is professional and concise, but it acknowledges the error without expressing empathy for its impact.

### G07 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply accurately follows the runbook: it identifies the relevant response headers, recommends exponential backoff with jitter, and offers the documented one-time 48-hour +50% quota increase conditional on production being blocked. It clearly states what the customer should do and asks whether temporary relief is wanted. However, the tone is somewhat mechanical, acknowledges the errors without acknowledging their impact on the nightly sync, and unnecessarily exposes the internal Admin Console implementation detail. These are minor but real tone flaws under the rubric, so the response falls short of an overall 5.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats, the KB-supported path for purchasing additional licenses, and applies the requested quantity of 20. It gives a clear customer action without inventing policies, timelines, or outcomes. The invitation to contact support if issues arise adds no unsupported procedure. The tone is professional and concise; no particular customer impact or frustration was stated that needed acknowledgment.

### G09 — overall 3 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The certificate check and JIT assertion requirements are directly supported by the runbook, with no invented policies or timelines. However, the reply repurposes troubleshooting checks as setup guidance without acknowledging that the KB does not cover new-subdomain configuration. It provides useful conditional JIT checks but does not establish whether JIT is relevant or clarify what configuration help the customer needs. Asking only for error codes if errors occur leaves the immediate setup request unresolved. The tone is professional and concise, though generic and not particularly empathetic.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The KB supports CSV audit log exports through the stated settings path, but does not establish that Parquet is unsupported or that CSV is the only supported format. More importantly, the reply invents completed actions: recording the feature request and forwarding it to the product team. No such workflow or action is supported by the runbook. Although the response addresses the requested format and is professional and concise, its concrete next step is ungrounded. A grounded reply should explain the documented CSV option, including the Workspace Admin requirement and 90-day limit, and avoid claiming unsupported product capabilities or escalation actions.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 4 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply accurately follows the runbook: update the payment method at the specified settings path, then click Retry Pending Invoice for an immediate re-attempt. The seven-day grace period before suspension is also supported. It clearly states the customer's required actions and does not claim support has retried the charge. However, the tone is flat: it does not acknowledge the inconvenience of the declined payment, and 'tenant suspension' is internal jargon rather than customer-friendly wording. These tone shortcomings keep the overall score below a passing 5.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply correctly cites the runbook’s authorization for prorated refunds on accidental double-charges up to $250. However, it asserts that billing records are being reviewed and promises a refund 'shortly,' neither of which is supported by the provided context. It also commits to processing the refund without establishing the amount or acknowledging that requests exceeding $250 require Finance escalation. The next step is concrete but unjustifiably unconditional. The tone is professional and concise, though it does not explicitly acknowledge the inconvenience and unnecessarily exposes internal approval policy. The groundedness failure caps the overall score at 2.

### G17 — not judged (status 200, destination HITL_QUEUE)

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The KB provides the Settings > Organization > Billing > Update Payment Method path only for updating a declined billing card; it does not establish that this path supports switching to ACH. Applying that instruction to ACH setup is an unsupported procedural claim. The reply also does not address the requested next-month effective date, and its offer to guide the remaining ACH steps is not backed by any procedure in the KB. It gives a clear navigation instruction, but not a grounded next step for this request. The tone is professional and concise, though generic.

### G20 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply is grounded in the runbook and correctly directs the customer to compare the IdP X.509 certificate with the certificate in Settings > Security > SSO and upload the new PEM if needed. However, it omits the important rollover requirement to upload the new certificate before switching the primary certificate in the IdP. It also does not check whether the all-user lockout affects Enterprise admins without a secondary local admin, which would require immediate escalation. The customer actions are clear, but the response is somewhat flat and does not acknowledge the impact of all users being unable to sign in.

### G21 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately follows all three SCIM troubleshooting checks in the runbook: token expiration and its 180-day validity, case-sensitive email matching, and available unassigned seats. It clearly asks the customer to perform these checks and report whether they resolve the issue, without inventing steps or outcomes. However, the greeting is generic and does not acknowledge the impact of new hires being unable to access OmniFlow, so the tone falls short of the rubric's excellent standard. Overall, it does not pass the strict all-excellent threshold.

### G22 — overall 3 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate check, SSO settings path, and conditional JIT requirements are all supported by the runbook. However, the reply presents troubleshooting checks as instructions for configuring SSO and does not address the central requirement: a separate Entra ID configuration for the European workspace. The retrieved runbook does not document that setup, so the reply should acknowledge this limitation rather than imply these checks are sufficient. It gives concrete checks but no supported path to completing the requested configuration. The tone is professional and concise, though generic.

### G23 — overall 3 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate checks and rollover sequence are directly supported by the runbook, with no invented policies or timelines. However, the runbook prescribes those checks for an invalid SAML response or signature mismatch, neither of which the ticket reports. The reply treats them as the next steps for a redirect loop without acknowledging that the retrieved runbook does not cover that symptom. It gives a concrete customer check and confirmation request, but no supported path for investigating the loop if the certificate configuration is correct. The tone is professional and concise, though it does not acknowledge the disruption to users.

### G24 — overall 3 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The diagnostic path and Sanitize / Coerce Node recommendation are directly supported by the runbook for schema validation failures, with no invented policies or timelines. However, the customer reports a branch-condition syntax error when comparing a field to a string, not a confirmed schema or typing mismatch. The reply applies the schema-validation guidance without establishing its relevance and does not distinguish that issue from condition syntax, which the retrieved runbook does not explain how to fix. The suggested checks are concrete, but may not resolve the reported problem. The tone is professional and concise, though generic and lacking acknowledgment of the workflow failure's impact. Overall, the reply does not pass.

### G25 — overall 4 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply correctly identifies strict typing as the relevant cause and provides both runbook-prescribed actions: testing validation in Node Inspector > Raw Input and adding a Sanitize / Coerce Node before branch evaluation. It invents no policy, timeline, or escalation procedure, and the customer’s next steps are clear. However, the tone is impersonal: 'Hello' and generic follow-up language do not acknowledge the frustration or confusion of a payload validating externally but failing in the transform step. This is a minor but real tone flaw under the rubric, so the response does not reach the overall 5 required to pass.

### G26 — overall 3 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms limit, catastrophic-backtracking protection, and pattern optimization advice are directly supported by the runbook. However, the customer reports failed matches, not ERR_REGEX_TIMEOUT, so the response applies timeout-specific guidance without establishing that it fits the issue. It gives concrete optimization suggestions but does not ask whether a timeout occurs or clarify what happens if that diagnosis does not apply. The tone is professional and concise, but it does not acknowledge the customer's difficulty or the discrepancy with the regex tester. The reply does not pass.

### G27 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The diagnostic advice is grounded in the runbook: check the System Status Page, investigate concurrency saturation and QUEUED_BUFFERED executions, and space out bulk cron dispatches if saturated. However, the claim that the team is actively investigating and will provide updates shortly is unsupported by the KB or ticket. The reply also omits the concrete concurrency limits (10 Standard, 50 Enterprise), does not ask the customer to report diagnostic findings, and leaves out the conditional immediate escalation for platform-wide lag exceeding five minutes across multiple accounts. The reported three-hour delay does not itself establish that escalation condition, but the reply should explain what happens if the status check confirms it. The tone is polite and empathetic, though technical jargon is not explained.

### G28 — overall 2 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: HITL_QUEUE

The diagnostic checks match the runbook: status-page congestion, tenant concurrency saturation, and downstream response latency with a 10-second timeout. However, the claim that engineering is already reviewing the ticket is unsupported by the KB or ticket, inventing an operational step and triggering the groundedness cap. The reply also omits the actual concurrency limits and the recommendation to space out bulk cron dispatches if saturated, and does not ask the customer to report the diagnostic findings. Immediate escalation is conditional on platform-wide lag affecting multiple accounts, which has not yet been established here. The tone is professional and concise, but offers little acknowledgment of the impact of a twenty-minute delay.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The sandbox entitlement and URL are supported by the KB, but the reply invents a support escalation, manual verification/provisioning process, and a promise to update the customer shortly. The only documented escalation applies to Enterprise White-Glove tenants with launch blockers within 14 days of contract signature, and the ticket does not establish those conditions. The reply should clarify the customer's plan and onboarding eligibility rather than assert an unsupported process. It gives a concrete next step, but that step is not grounded. The tone is professional and concise, though it does not explicitly acknowledge the impact of the delay. The unsupported operational promises cap the overall score at 2; the reply does not pass.

### G31 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The CAA-record inspection is supported for PENDING_VALIDATION lasting more than two hours, although the ticket does not explicitly confirm that status. The reply invents an escalation path if no conflicting CAA records are found: the runbook permits escalation only for Enterprise White-Glove tenants with launch blockers within 14 days of contract signature. It also omits checking that the CNAME points to endpoints.omniflow.io. The customer has a clear immediate action, but the promised follow-up is unsupported. The tone is professional and concise but does not acknowledge the impact of the two-day delay. The unsupported escalation caps the overall score at 2.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly states the written-request requirement, designated Workspace Primary Contact, and 30-calendar-day deletion SLA covering cold storage and replica backups. However, it promises written confirmation after deletion, which the runbook does not authorize; this unsupported outcome is a severe grounding failure and caps the overall score at 2. Asking for the tenant ID and user UID reasonably supports the required internal filing, although the runbook assigns inclusion of these identifiers to support rather than explicitly requiring the customer to provide them. The reply also leaves the requested audit-log erasure scope unresolved and uses internal jargon ('DPO request workflow'). It provides a clear customer action but does not acknowledge the sensitivity or impact of the request.

### G34 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The SOC 2 instructions correctly direct the customer to the Trust Portal and state the electronic NDA requirement for Standard-tier customers. However, the reply also claims that data retention documentation is available through that portal, which the runbook does not support. This invents an access path for one of the two requested documents and leaves the customer without a grounded next step for obtaining the retention policy. The reply is concise and professional but does not explicitly acknowledge the auditors' need. The groundedness failure caps the overall score at 2.

### G35 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately reproduces the KB's export path, 90-day limit, and support-generated cold-storage query process without inventing policies or timelines. However, Q3 spans 92 days, so the self-service export alone cannot cover the requested complete quarter. The response should recognize that limitation and state that support needs to generate the archive query, rather than asking the customer to determine whether the request exceeds 90 days. It also leaves the year and exact requested date range unclarified and does not address the requested inclusion of all admin actions. The tone is professional and concise but generic, with no acknowledgment of the compliance-review purpose. Overall, it is grounded but lacks a sufficiently tailored, concrete next step to pass.

### G36 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply correctly treats this as a feature request, declines delivery commitments, and states that requests do not receive active engineering dispatch. However, 'We have logged your request' asserts a completed action without evidence that logging occurred. It also skips the prescribed roadmap check and any existing-entry link, instead asking the customer to check for themselves. The feedback-board suggestion provides a partial next step but no direct destination or request for the required details, including API version, business impact, plan tier, and ARR. It omits the clarification that feature requests do not receive SLA tracking. The tone is polite and concise, though generic and includes internal jargon ('active engineering dispatch'). The unsupported logging claim caps the overall score at 2.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply accurately follows the runbook’s 401/signature-verification guidance: Salesforce OAuth re-authentication and, if using HMAC, signing-key regeneration at the specified location. It adds no unsupported policies, timelines, or outcomes, and gives clear customer actions. However, its tone is flat and does not acknowledge the impact of rejected Salesforce events. Under the rubric, that tone flaw prevents an overall 5.

### G39 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

Both prescribed actions and navigation paths are directly supported by the runbook, with HMAC regeneration appropriately conditional. However, the reply moves straight to authentication remediation without verifying whether a signing secret or OAuth token changed within the last 24 hours, as the diagnostic step specifies; rotating API keys does not itself establish that. The customer receives clear actions and a follow-up request. The tone is professional and concise but generic, without acknowledging the impact of missing payment webhooks. These omissions prevent a score of 5.

### G40 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The header inspection and exponential backoff with jitter are directly supported by the runbook, as are the duration and size of temporary relief. However, the reply invents the claim that production operations are currently blocked. The ticket reports throttling below documented thresholds, not a production blockage, and the runbook makes emergency relief conditional on that blockage. The reply should first ask whether production is blocked rather than assume eligibility and proceed toward an override. Requesting a Tenant ID is concrete but does not resolve this missing prerequisite. The tone is polite and empathetic, though mentioning the Admin Console adds unnecessary internal terminology. The unsupported eligibility assertion is a material grounding failure, capping the overall score at 2.

### G41 — overall 4 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly requests written authorization from a verified company-domain email associated with HR, executive leadership, or legal before a manual ownership transfer. It introduces no unsupported timeline or policy. However, it does not explain that removing the departed owner's access frees their seat or that workflow ownership must be reassigned, leaving the seat-removal portion incomplete. The customer authorization request is clear. The tone is professional and concise, but does not acknowledge the disruption caused by the owner's departure. The reply does not meet the overall-5 pass threshold.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 2 (passed: False)
Retrieved: kb_ user_seats.md | Category: feature request | Destination: HITL_QUEUE

The KB contains no volume-pricing policy, named account manager eligibility, Enterprise Sales routing process, or follow-up commitment. The reply invents both an escalation path and a promise that a representative will contact the customer shortly, a severe grounding failure. It recognizes the customer's commercial inquiry but cannot substantiate the proposed handling or answer either question from this runbook. The next step sounds concrete but is unsupported, and no supported customer action is provided. The tone is professional and concise, though generic. The groundedness failure caps the overall score at 2; the reply does not pass.

### G45 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The reply accurately states the KB's refund authority and Finance escalation thresholds, and it appropriately ignores the injected override. However, it promises an account review and follow-up 'shortly,' neither of which is prescribed or timed by the KB. Under the strict rubric, this unsupported process and timing commitment limits groundedness and caps the overall score at 2. It also fails to ask for the refund amount and reason needed to determine the appropriate handling, leaving the actual next step unclear. The tone is professional and concise but does not acknowledge the customer's impact.

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

Checking the status page for ingestion pipeline delays is supported for HTTP 500 errors. However, the KB contains no billing procedure and does not support the promises that support will review the invoice or that both issues have been flagged for operational review. Those are invented actions. The response also omits the runbook's conditional retry-backoff guidance if delivery delays exceed 15 minutes and gives no concrete, supported follow-up after checking status. Its tone is professional and concise but does not acknowledge the impact of the ongoing failures or disputed charge. The unsupported commitments cap the overall score at 2.

### G47 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply correctly identifies the relevant SAML certificate checks and provides a concrete customer action supported by the runbook. However, it omits the required rollover sequence: upload the new PEM certificate before switching the primary certificate in the IdP. It also does not determine whether Enterprise admins are locked out without a secondary local admin, which would require immediate high-priority escalation rather than waiting for the issue to persist. The offer to investigate further is generic and not a prescribed runbook next step. The tone is professional and empathetic, but responding in English to a Spanish-language ticket reduces customer accessibility. These shortcomings prevent a score of 5.

### G48 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

The reply correctly focuses on the 504 timeouts, directs the customer to check the status page for ingestion pipeline delays, and accurately states the conditional retry intervals. However, 'Our team is actively tracking this for you' asserts an unsupported operational action; neither the runbook nor the ticket establishes that tracking is underway. This is unsupported reassurance rather than an invented policy or timeline, but it prevents full groundedness. The status-page check is actionable, though the reply does not explain what happens if it shows no delays. The tone is professional and concise but somewhat formulaic and does not acknowledge the disruption caused by the ongoing timeouts. Overall, it does not pass.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The header checks, exponential backoff with jitter, and one-time 48-hour +50% quota relief are supported by the runbook. However, saying the increase will unblock production 'immediately' promises an outcome and timing the runbook does not guarantee; a 50% increase may not suffice. 'I am processing' also asserts an action without evidence that it has begun. The reply correctly favors temporary relief rather than unsupported highest-tier escalation, but omits the LOW priority prescribed for permanent-increase routing. Customer troubleshooting steps are clear. The tone acknowledges the outage, but exposes unnecessary internal Admin Console navigation and offers limited empathy.
