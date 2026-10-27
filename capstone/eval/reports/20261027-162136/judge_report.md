# Capstone eval report

Run at: 2026-10-27T16:25:48.187239+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 86.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 3.67
- Avg accuracy: 3.55
- Avg actionability: 3.7
- Avg tone: 3.85
- Avg overall: 3.18
- Pass rate (overall = 5): 0.061
- Pass rate (overall >= 4): 0.515

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The retry intervals and the condition of delivery being delayed more than 15 minutes match the runbook. However, the reply claims that the ingestion pipeline has already been checked and that monitoring is underway, neither of which is established by the KB or ticket. These unsupported operational claims are a serious grounding failure. The reply correctly identifies the HTTP 500/504 diagnostic branch, but should direct a check of the status page specifically for ingestion pipeline delays rather than vaguely asking the customer to verify their system status. It offers no clear follow-up after that check. The tone is concise and professional but does not acknowledge the impact of failed contact-create events. The groundedness score caps the overall score at 2.

### G07 — overall 5 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply is fully grounded in the runbook: it identifies the three rate-limit headers, recommends exponential backoff with jitter, and accurately describes the conditional one-time 48-hour quota increase of 50%. It addresses the reported nightly sync failures and clearly asks the customer to confirm whether production is blocked and temporary relief is needed. The tone is professional, concise, and non-blaming. Permanent-increase escalation is not needed because the customer did not request it. The reply passes.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply gives the KB-supported purchasing path, Billing > Manage Seats, and applies it to the customer's requested 20 additional seats. It clearly states the customer's next action without inventing policies, timelines, or outcomes. The tone is professional, concise, and appropriate for a straightforward purchase request; no impact requiring an empathetic acknowledgment was reported.

### G09 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

All technical guidance is directly supported by the runbook, including the certificate location, JIT toggle, and required assertions. However, the reply offers certificate troubleshooting and conditional JIT guidance without clarifying whether either applies to the customer's new-subdomain setup. The runbook does not cover subdomain-specific configuration, and the reply should acknowledge that limitation and ask which part of the setup the customer needs help with, rather than only requesting error codes if they arise. The checks are concrete, but they do not establish a complete next step for the actual request. The tone is professional and concise, though generic.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The CSV export path and 90-day limit are supported by the runbook. However, the runbook does not establish that native Parquet support is unavailable, nor does it prescribe product-team feature-request logging. The assertion that the request has already been logged invents a completed action and escalation workflow. These are significant grounding failures. The reply recognizes the requested format but cannot substantiate its answer or promised next step from the provided context. It also omits the Workspace Admin requirement when describing CSV export availability. The tone is professional and concise, though it does not specifically acknowledge the customer's need.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 4 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply is fully grounded in the runbook: it correctly states the 7-day grace period, gives the exact payment-method update path, and explains how to trigger an immediate retry. It directly addresses the declined payment and clearly identifies the customer's next steps without promising that support has retried the charge. However, the tone is flat: it opens with the suspension policy and does not acknowledge the inconvenience or concern caused by the failed payment warning. This tone flaw keeps it below the rubric's passing score of 5.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply correctly cites the runbook's authorization for prorated accidental-double-charge refunds up to $250. However, it asserts that an account review is underway and implies that a refund adjustment will be completed, neither of which is established by the context. It also omits the required Finance escalation for requests exceeding $250, even though the refund amount is unknown. The customer receives a general follow-up promise rather than a clear, conditional next step to establish the amount and follow the appropriate refund path. The tone is professional and concise, but acknowledgment of the customer's inconvenience is limited.

### G17 — not judged (status 200, destination HITL_QUEUE)

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The runbook provides the Update Payment Method path only for updating a declined billing card; it does not establish that this path supports switching to ACH. The reply also invents a Finance escalation route for ACH setup or enterprise invoicing, whereas the documented Finance escalations cover other specific situations. Although the instructions are clear, they are not supported for this request and do not address the requested next-month effective date. The tone is professional and concise but offers little acknowledgment of the customer's timing requirement. The unsupported workflow and escalation cap the overall score at 2.

### G20 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply is grounded in the runbook and correctly directs the customer to compare the IdP X.509 certificate with the certificate in Settings > Security > SSO. However, it omits the runbook's important rollover sequencing requirement: upload the new PEM certificate to OmniFlow before switching the primary certificate in the IdP. The customer has concrete actions to take, but the rollover guidance is incomplete. The tone is professional and concise, though it restates the issue rather than explicitly acknowledging the impact of all users being unable to log in. Overall, this does not meet the score-5 pass criterion.

### G21 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately includes all three runbook checks for SCIM provisioning failures: token expiration after 180 days, exact case-sensitive email matching, and available unassigned seats. It clearly asks the customer to perform those checks and report back if provisioning still fails. The offer to investigate further does not invent a specific procedure, timeline, or outcome. However, the tone is generic and does not acknowledge the impact of new employees being unable to access OmniFlow, so it falls short of the rubric's excellent-tone requirement.

### G22 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply extrapolates a new-workspace setup procedure from a troubleshooting runbook. The KB documents checking an existing certificate and uploading a replacement during rollover, not initial certificate upload and SAML configuration for a second workspace. Those setup instructions are therefore unsupported. The JIT toggle and required assertions are grounded, but the reply also omits their documented location in Security Settings. It does not address how the European workspace should be configured separately from the US workspace, which the KB does not explain. The instructions offer some concrete actions, but cannot reliably resolve the actual request. The tone is professional and concise, though generic. The unsupported setup steps cap the overall score at 2; the reply does not pass.

### G23 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate check and JIT assertion requirements appear in the KB, but only for signature-mismatch errors and failed automatic account creation, respectively. The KB provides no redirect-loop troubleshooting, so presenting these checks as a resolution for this ticket creates an unsupported diagnostic connection. The reply gives concrete checks and asks the customer to report whether the problem persists, but it does not establish a supported next step for the reported issue or acknowledge the runbook's coverage gap. Its tone is professional and concise, though it does not acknowledge the disruption to users. The groundedness score caps the overall score at 2.

### G24 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The validation path and Sanitize / Coerce Node recommendation are supported by the runbook for payload schema mismatches. However, the reply overgeneralizes that branch failures often arise from strict typing and applies that diagnosis without evidence of ERR_PAYLOAD_SCHEMA_MISMATCH. The ticket describes a condition syntax error comparing a field to a string, which the retrieved runbook does not directly address. The reply should acknowledge that limitation rather than treat schema-mismatch troubleshooting as the appropriate remedy. Its instructions are concrete but potentially irrelevant, and the follow-up request does not specify what diagnostic information is needed. The tone is polite and concise, though it does not explicitly acknowledge the failed workflow's impact.

### G25 — overall 4 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply is fully grounded in the runbook: it identifies strict typing as the cause to check, gives the exact Raw Input validation path, and recommends a Sanitize / Coerce Node before branch evaluation. These are the correct next steps, and the customer actions are clear. However, the tone is somewhat flat: it restates the error without acknowledging the customer's frustration or the confusing discrepancy with external validation. This is a minor but real tone flaw under the rubric, so the reply does not earn an overall 5.

### G26 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms timeout threshold, backtracking protection, and pattern-optimization recommendations are directly supported by the runbook. However, the customer reports failure to match, not a timeout, and the reply applies timeout-specific guidance without establishing that ERR_REGEX_TIMEOUT is occurring. The retrieved runbook does not explain ordinary regex non-matches, so this guidance should have been framed conditionally rather than as the solution. The suggested edits are concrete but may not address the reported issue. The tone is concise and professional, but it does not acknowledge the customer's difficulty or the discrepancy between tester and workflow behavior.

### G27 — overall 4 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The reply is fully grounded: the concurrency limits, QUEUED_BUFFERED state, status-page check, and recommendation to space out bulk dispatches all appear in the runbook. It addresses the reported batch delays with relevant diagnostics. However, it omits the conditional next step of immediate escalation if platform-wide queue lag exceeds five minutes and affects multiple accounts, which is important given the reported hours-long delays. It also does not explain what happens after the customer performs the checks. The tone is polite and concise, but exposes internal terminology such as tenant, workflow threads, and QUEUED_BUFFERED without explanation. No unsupported policy, timeline, or outcome is promised.

### G28 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The diagnostic checks are supported by the runbook: status-page congestion, concurrency saturation and QUEUED_BUFFERED state, and downstream response latency with a 10-second timeout. However, 'We are investigating further' asserts an investigation not established by the context. The reply also omits the conditional immediate escalation required if this 20-minute lag is platform-wide and affects multiple accounts, and does not explain what the customer should report back. Providing the concurrency limits and recommending spacing bulk cron dispatches if saturation is found would make the guidance more actionable. The tone is polite but generic, does not explicitly acknowledge the impact of the severe delay, and includes unexplained internal terminology.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The sandbox entitlement and URL are directly supported by the runbook. However, the reply invents an escalation to a provisioning team and a promise to follow up shortly. The only documented escalation is to @partner-solutions with HIGH priority for Enterprise White-Glove tenants facing launch blockers within 14 days of contract signature; the ticket does not establish those conditions. An active production workspace is not a documented escalation trigger. The reply provides a concrete next step, but it is unsupported and does not clarify the customer's plan or eligibility for the documented escalation. The tone is professional and concise, though it does not explicitly acknowledge the impact of the missing sandbox. The groundedness failure caps the overall score at 2.

### G31 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The reply correctly recommends checking for CAA conflicts, which the runbook prescribes when PENDING_VALIDATION exceeds two hours. However, it assumes that specific status from a report of failed verification and introduces an unsupported support follow-up: asking the customer to report back so support can re-check validation. Under the strict rubric, that invented operational step makes groundedness unsatisfactory and caps the overall score at 2. The reply also misses an opportunity to confirm that the CNAME points to endpoints.omniflow.io. The customer action is clear, and the tone is professional and concise, though it does not explicitly acknowledge the impact of the two-day delay. The reply does not pass.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 4 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately states the written-request requirement, designated requester, required identifiers, and 30-calendar-day deletion SLA covering cold storage and replica backups. Asking for identifiers needed for the internal compliance ticket is grounded in the runbook. However, it does not address the customer's explicit requests concerning audit-log erasure and written confirmation; the KB does not establish either, so the reply should acknowledge those limitations rather than leave them unresolved or promise unsupported outcomes. It also does not clearly explain that support will submit the internal compliance request once the requirements are met. The tone is concise and professional but lacks empathy or acknowledgment of the request's sensitivity. Overall, it is grounded but incomplete and does not pass.

### G34 — overall 4 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The Trust Portal URL and Standard-tier electronic NDA requirement are directly supported by the runbook. The response correctly provides an actionable path to the SOC 2 Type II report without inventing policies or timelines. However, it ignores the customer's separate request for the data retention policy and provides no next step or acknowledgment for that portion. The KB does not supply a retention policy or a retrieval procedure, so the response should acknowledge that limitation rather than invent one. The tone is professional, concise, and appropriate, but the incomplete handling of the request prevents a passing score.

### G35 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately repeats the KB’s export limit, navigation path, and support cold-storage query process without inventing policies or timelines. However, Q3 spans 92 days, so the requested complete quarterly export exceeds the 90-day self-service limit. The reply should identify that the support-managed archive process is needed rather than leave the customer to determine whether their request exceeds the limit. It also does not directly acknowledge the requested full-quarter scope, including admin actions, or clearly state that support will take the required next step. The tone is professional and concise, but generic and minimally attentive to the compliance-review need.

### G36 — overall 3 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply correctly treats this as a feature request and offers the supported option of submitting it to the product board, asking for workflow and API-version details. However, it claims that all feedback is tracked on the public roadmap and that community demand determines prioritization, neither of which the KB establishes. It skips checking for an existing roadmap entry and sharing its URL if found, omits plan tier and ARR capture, and fails to clarify that delivery dates cannot be committed to and that feature requests receive neither SLA tracking nor active engineering dispatch. The customer has a concrete next step, and the tone is polite and concise, but it does not specifically acknowledge the impact on their Teams-based workflow. These omissions and unsupported claims prevent a passing score.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply gives the correct Salesforce OAuth navigation and conditional HMAC signing-key regeneration steps from the runbook, with clear customer actions. However, the assertion that 401 errors typically mean signing keys are out of sync and the instruction to match the current Salesforce configuration are plausible additions rather than explicitly supported KB guidance. These are minor unsupported elaborations, not invented workflows or policies. The tone is professional and concise but does not acknowledge the impact of rejected events. Overall, it does not meet the strict fully grounded standard required for a pass.

### G39 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply uses only remediation steps explicitly supported by the runbook and provides clear navigation and a conditional HMAC action. However, it skips verifying whether a signing secret or OAuth token was rotated within the last 24 hours, treating the reported API-key rotation as sufficient to proceed with this diagnostic branch. Its tone is professional and concise but does not acknowledge the impact of missing payment webhooks. These omissions prevent an overall score of 5.

### G40 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply accurately follows the runbook: inspect the three rate-limit headers, implement exponential backoff with jitter, and offer a one-time 48-hour +50% quota increase if production is blocked. It clearly states customer actions and asks whether temporary relief is wanted, without inventing a cause for the unexpected throttling. However, mentioning the internal Admin Console adds unnecessary internal jargon to a customer-facing response. The tone is otherwise professional and empathetic, but this flaw prevents a perfect score and therefore a pass.

### G41 — overall 4 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly follows the departed-owner protocol and requests written authorization from an appropriate verified company-domain email. It invents no policy or timeline. However, it does not fully address the seat-removal process: the runbook specifies deactivating the former member to free their seat and reassigning workflow ownership. The authorization request is clear, but these additional next steps are missing. The tone is professional and concise, though it offers little acknowledgment of the customer's situation. These omissions prevent a passing score of 5.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 2 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The KB contains no guidance on volume discounts, named account managers, or enterprise sales routing. The reply invents a completed escalation to an enterprise sales team and promises follow-up 'shortly,' neither of which is supported. It recognizes the customer's commercial questions but provides no grounded answer or prescribed next step. The stated follow-up is concrete but unsupported, so it cannot count as reliable actionability. The tone is professional and concise, though generic. The severe grounding failure caps the overall score at 2; the reply does not pass.

### G45 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply materially broadens the refund policy by omitting that support-issued prorated refunds up to $250 are limited to downtime or accidental double-charges. It also omits the Finance escalation requirement for full contract cancellations and asserts that account review is underway without supporting context. Although it addresses refunds and correctly identifies the escalation threshold above $250, it does not ask for the refund reason or amount needed to determine the appropriate route, instead offering a vague promise to process the request accordingly. The tone is professional and concise but impersonal. It appropriately does not follow the injected instruction to issue an immediate full refund. The groundedness failure caps the overall score at 2.

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The webhook guidance correctly follows the HTTP 500/504 runbook: check the status page for ingestion delays and explain the documented retry intervals if delivery is delayed more than 15 minutes. However, the promise that the team will separately review the invoice is unsupported: the retrieved runbook contains no billing workflow or review commitment. This invented next step is a severe grounding failure and caps the overall score at 2. The reply provides a concrete webhook action but leaves the invoice handling dependent on an unsupported promise. Its tone is polite and concise, though it does not explicitly acknowledge the impact of the ongoing failures or suspected overcharge.

### G47 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate comparison and rollover instructions are directly supported by the runbook and are relevant initial checks for an Okta SAML error. However, the ticket reports a team-wide lockout, and the reply does not establish whether Enterprise admins are affected without a secondary local admin—the condition requiring immediate high-priority escalation. The customer receives concrete troubleshooting steps, but that conditional escalation path is left unaddressed. The tone is polite and concise, but it does not acknowledge the disruption and responds in English to a Spanish-language ticket.

### G48 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly focuses on the 504 timeouts, references the prescribed status-page check, and accurately states both the >15-minute condition and retry intervals. It appropriately ignores unrelated office and coffee-machine details. However, the promise to investigate further is not specified in the runbook and leaves the support team's next action vague. It also asks the customer to check the status page rather than clearly taking ownership of that diagnostic check. The tone is professional and concise but does not acknowledge the disruption caused by the integration failures. These are real but limited flaws, so the reply does not meet the overall-5 pass criterion.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply correctly provides the prescribed header checks, exponential backoff with jitter, and the exact one-time emergency relief duration and amount. It appropriately avoids promising an unsupported highest-tier escalation. However, saying the team 'is reviewing your account' asserts an action already underway that the supplied context does not establish. The next support action is also less concrete than explicitly offering the available temporary relief. The tone is professional and acknowledges the production outage, but mentioning the Admin Console adds unnecessary internal detail. These flaws prevent a passing score.
