# Capstone eval report

Run at: 2026-11-02T17:25:09.463109+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 86.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 3.61
- Avg accuracy: 3.48
- Avg actionability: 3.48
- Avg tone: 3.79
- Avg overall: 3.27
- Pass rate (overall = 5): 0.212
- Pass rate (overall >= 4): 0.424

## Judge (triage decisions)
- Cases judged: 33
- Avg t_category_fit: 4.88
- Avg t_priority_calibration: 4.7
- Avg t_action_needed: 4.76
- Avg t_issue_completeness: 5.0
- Avg t_overall: 4.42
- Pass rate (overall >= 4): 0.879
- Pass rate (overall = 5): 0.636

## Costs
Prices as of 2026-11-02 (USD); token counts measured, not estimated.
- Run total: $0.3121
- Generator: $0.0264 | Judge: $0.2845 | Embeddings (queries): $0.0004 | Index build: $0.0008
- Per ticket (automated): mean $0.000814 (n=16)
- Per ticket (deflected): mean $9e-06 (n=10)
- Per ticket (human_queue): mean $0.000806 (n=17)
- Kestra daily projection (30d): $9.36

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly identifies checking the status page as the next step for HTTP 500 errors and reproduces the retry intervals accurately. However, it omits the prerequisite that delivery be delayed more than 15 minutes before presenting the retry guidance. More importantly, it implies escalation after 30 minutes of validation failures without the runbook’s required condition that failures occur across multiple tenants, creating an unsupported escalation promise. The customer has a concrete status-page check and follow-up request, but the reply does not establish whether validation failures are actually occurring. The tone is professional and concise, though it offers little acknowledgment of the customer’s impact. The groundedness failure caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category correctly identifies a HubSpot webhook delivery failure; the space-separated label is semantically equivalent to integration_webhook_failure. Medium priority fits a single-integration error with no stated production-wide outage or core-business disruption. The active HTTP 500 error requires action. No secondary issues are reported, so the empty list is correct. The draft reply is outside the scope of this evaluation.

### G07 — overall 4 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply correctly addresses 429 throttling and recommends the runbook's response-header monitoring and exponential backoff with jitter. It accurately describes the production-blocked condition and the 48-hour, +50% temporary increase, but omits the important one-time restriction. Its request to proceed with relief is concrete, though it should explicitly ask whether production operations are blocked. The tone is professional and concise, but only lightly empathetic, and mentioning the internal Admin Console is unnecessary customer-facing detail. These are limited shortcomings rather than invented remediation or an unsupported promise.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to quota_rate_limit_exceeded, despite using a human-readable label rather than the canonical identifier. Medium priority is appropriate for a nightly batch sync encountering 429 errors without evidence of critical-flow blockage or broader operational degradation. The active error correctly requires action. The ticket describes only one issue, so an empty secondary_categories list is complete.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats to purchase the requested 20 additional licenses, matching the runbook without inventing policies, timelines, or outcomes. It gives a clear customer action and stays focused on the seat-expansion request. The tone is professional and concise, though somewhat generic rather than especially warm; no significant customer impact was stated that needed acknowledgment.
Triage: overall 4 (passed: True) - User seat management is the best fit for expanding workspace licenses, although the category should use the canonical value user_seat_management. Low priority is defensible because no operational blockage is reported, but medium is better aligned with the guidelines for billing-related account updates and license purchases. action_needed=true correctly identifies an explicit account-modification request. There is only one support issue, so an empty secondary_categories list is correct.

### G09 — overall 4 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply stays within the runbook: the certificate location and matching requirement, JIT toggle, and required firstName, lastName, and email assertions are all supported. It correctly makes JIT guidance conditional and invents no subdomain configuration steps or promises. However, these are general checks rather than a complete answer to the new-subdomain setup request; it does not acknowledge that the retrieved runbook lacks subdomain-specific instructions or clarify whether JIT is the customer's goal. The checks and request for specific errors provide concrete next actions, though the follow-up could be better targeted. The tone is professional and concise but somewhat generic.
Triage: overall 5 (passed: True) - The primary category correctly identifies Okta SAML configuration as auth_sso_provisioning, despite the alternate label formatting. Low priority is appropriate for setup assistance with no reported login failure, lockout, or production impact. Action is needed because the customer requests assistance configuring authentication. The new subdomain is context for the SAML setup, not a separate domain-routing issue, so no secondary categories are warranted.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The CSV export instructions and 90-day limit are supported by the runbook. However, the runbook does not establish that Parquet is unsupported, and the claim that the request has been logged with the product team invents both an escalation step and a completed action. These are substantive grounding failures. The reply recognizes the feature request but cannot substantiate its answer or promised next step; CSV is a grounded alternative, not a resolution to the requested format support. The tone is professional and concise, though acknowledgment of customer impact is limited. The groundedness failure caps the overall score at 2.
Triage: overall 2 (passed: False) - The primary category correctly identifies a request for a new export format, rather than an audit-log retrieval issue. Low priority is appropriate for a feature request, and no secondary issues are present. However, action_needed should be true: the customer explicitly asks for a product capability to be added, an unresolved actionable request requiring product review rather than an acknowledgment or informational message. The category label should also use the defined identifier feature_request instead of feature request.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 5 (passed: True)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply is fully supported by the runbook: it gives the correct payment-method update path, directs the customer to Retry Pending Invoice for an immediate retry, and accurately states the 7-day grace period. It directly addresses the declined payment and clearly assigns the next steps to the customer without implying support has already retried the charge. The tone is professional and concise, but lacks acknowledgment of the inconvenience and uses the internal-sounding term 'tenant suspension.' These are minor tone shortcomings rather than substantive issues.
Triage: overall 5 (passed: True) - The primary category correctly identifies a billing/subscription issue, despite using spaces rather than underscores in the category label. Medium priority fits a declined invoice payment without a reported service interruption. Action is needed because the customer explicitly requests a charge retry. The failed-payment warning is a symptom of the same billing issue, so no secondary categories are warranted.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply correctly cites support’s authority to issue prorated refunds for accidental double-charges up to $250. However, it invents an ongoing billing-record review and promises to process the refund shortly, neither of which is supported by the runbook. It also commits to a refund without establishing the amount or accounting for the required Finance escalation above $250. The next step sounds concrete but is not appropriately conditional on the authorization limit. The tone is polite and concise, though the internal authorization language is unnecessary for the customer. The groundedness failure caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category correctly identifies a billing subscription issue: a duplicate subscription charge and refund request. Medium priority fits a billing issue with no stated operational outage or urgent business impact. Action_needed=true is correct because the customer requests a refund requiring account action. The duplicate invoices and duplicate charge describe one issue, so an empty secondary_categories list is appropriate. The category's space-separated wording is semantically equivalent to the defined label. Draft reply claims are outside this evaluation's scope.

### G17 — not judged (status 200, destination HITL_QUEUE)

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply uses a navigation path present in the runbook, but that path is prescribed only for updating a billing card after a declined payment. The KB does not establish that customers can switch to ACH through that page, so presenting it as the ACH conversion procedure is an unsupported step. The reply also does not address the requested effective date of next month or explain that the retrieved guidance does not cover this change. It gives a concrete instruction, but not a supported next step for the actual request. The tone is professional and concise, though generic.
Triage: overall 5 (passed: True) - The primary category correctly identifies a billing payment-method change (despite using spaces instead of underscores). Medium priority matches the guideline for billing update inquiries. Action is needed because the customer requests an account modification. The ticket contains only one support issue, so no secondary categories are warranted. The draft reply is outside the scope of this evaluation.

### G20 — overall 4 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately reproduces the runbook's certificate-matching check and certificate-rollover sequence without inventing policies or timelines. It gives the customer a clear initial action. However, because all users are affected, it should clarify whether Enterprise admins are locked out with no active secondary local admin; that condition requires immediate escalation, which the reply omits. The tone is professional and concise but does not acknowledge the impact of the organization-wide login failure.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to auth_sso_provisioning, despite using a display-style label rather than the canonical identifier. Failed Okta SAML authentication for all users warrants high priority under the explicit SSO lockout guidance. action_needed=true correctly reflects an active, unresolved authentication error. There is only one distinct issue; the invalid assertion is its error detail, and the metadata update is background context, so no secondary categories are needed.

### G21 — overall 5 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately reproduces all three SCIM troubleshooting checks prescribed by the runbook: bearer-token expiry and its 180-day validity, exact case-sensitive email matching, and available unassigned seats. It introduces no unsupported policies, steps, timelines, or promises. The customer is clearly asked to perform these checks and report whether the issue persists. The tone is professional and concise, though it could better acknowledge the impact of new hires being unable to access OmniFlow.
Triage: overall 4 (passed: True) - The primary category correctly identifies an Okta/SCIM provisioning failure, despite using a display-style label rather than the canonical category identifier. Action is required because automatic provisioning remains broken, and no secondary issues are reported. Medium priority is defensible because the ticket does not establish an existing-user lockout or broad operational disruption, although high could be warranted if the provisioning failure blocks new employees from accessing essential workflows.

### G22 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply uses several KB-supported checks, including certificate matching and enabling JIT for automatic account creation. However, it incorrectly presents token validity and email matching as checks for either SAML errors or SCIM failures; the runbook assigns those checks specifically to SCIM failures. It also replaces the precise requirement that email match the OmniFlow account address exactly and case-sensitively with the unsupported phrase 'match your workspace settings.' More importantly, the customer needs initial Entra SSO configuration for a separate European workspace, while the reply provides troubleshooting checks without explaining that the retrieved KB does not cover separate-workspace setup. It offers no concrete path to obtaining the missing setup guidance. The tone is professional and concise but generic and does not acknowledge the customer's need to keep the workspaces separate.
Triage: overall 5 (passed: True) - The primary category correctly identifies an Entra ID SSO configuration request as auth_sso_provisioning; the differently formatted label is semantically equivalent. Low priority is appropriate for non-blocking initial setup with no reported authentication failure or production impact. Action is needed because the customer requests SSO configuration for a workspace. The European workspace and its separation from the US workspace are context for that single request, not additional support issues, so no secondary categories are warranted.

### G23 — overall 3 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate and conditional JIT checks are supported by the KB, and the reply invents no timeline or policy. However, the runbook does not identify either check as a remedy for redirect loops: certificate checks apply to signature errors, and JIT checks apply to failed automatic account creation. The reply should acknowledge that limitation rather than present these as established troubleshooting for this symptom. It also omits the required firstName, lastName, and email assertions and the instruction to upload the new certificate before switching the IdP's primary certificate. The customer receives concrete checks, but no clearly supported next step for the reported loop. The tone is professional and concise, though it does not acknowledge the disruption to users.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to auth_sso_provisioning, despite its noncanonical formatting. A Google Workspace SSO redirect loop is an authentication failure, so high priority is appropriate under the explicit SSO lockout guidelines. The active login error requires action. The ticket contains only one issue, correctly leaving secondary_categories empty.

### G24 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The navigation path and Sanitize / Coerce Node recommendation are supported by the runbook for schema validation failures. However, the reply makes an unsupported diagnostic claim that this branch-condition syntax error typically results from ERR_PAYLOAD_SCHEMA_MISMATCH. The ticket reports a syntax error comparing a field to a string, not evidence of strict-typing failure, and the runbook does not establish that connection or provide condition-syntax guidance. Thus, the response prematurely applies a different issue's troubleshooting steps rather than acknowledging the information gap and requesting the condition and exact error. The instructions and follow-up request are clear, but the tone is generic and does not acknowledge the workflow failure's impact. The unsupported diagnosis caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to workflow_syntax_execution_error: the customer reports a syntax error in a branch condition. Medium priority is appropriate for an isolated workflow failure with no stated broader production impact. action_needed=true correctly reflects an active unresolved error. The ticket contains only one support issue, so an empty secondary_categories list is complete. The draft reply is outside the scope of this evaluation.

### G25 — overall 5 (passed: True)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply accurately follows the JSON schema validation runbook: it explains strict typing mismatches, provides the exact Raw Input inspection path, and recommends a Sanitize / Coerce Node before branch evaluation. It introduces no unsupported policy, timeline, or promised outcome, and gives clear customer actions. The tone is professional and concise, though it could better acknowledge the frustration of a payload validating externally but failing in the workflow.
Triage: overall 5 (passed: True) - The primary category semantically matches workflow_syntax_execution_error exactly: JSON schema validation failures within a transform step are explicitly covered. Medium priority is appropriate for an isolated workflow error with no reported broader outage or critical business impact. Action_needed is correctly true because the customer reports an active, unresolved error. No secondary issues are present; external validation is context for the same failure, not a separate support issue.

### G26 — overall 3 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms threshold, catastrophic-backtracking protection, and recommendations about anchors and nested quantifiers are directly supported by the runbook. However, those recommendations concern regex timeouts, while the customer reports non-matching results without any timeout indication. The reply presents timeout-specific advice without acknowledging that the retrieved runbook does not establish the cause of this issue. Testing an updated regex in Workflow Builder is also not explicitly prescribed by the regex section. The customer receives concrete editing suggestions, but no grounded path for diagnosing the reported mismatch. The tone is concise and professional but does not acknowledge the customer's difficulty.
Triage: overall 5 (passed: True) - The primary category correctly identifies a regex failure within a workflow, matching workflow_syntax_execution_error despite the human-readable label formatting. Medium priority is appropriate for an isolated workflow error with no stated broader production impact. The active, unresolved extraction failure correctly requires action. The ticket contains only one support issue, so an empty secondary_categories list is complete. The draft reply is outside the scope of this evaluation.

### G27 — overall 2 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The reply correctly cites the status-page check, concurrency limits, QUEUED_BUFFERED state, and 10-second timeout. However, it asserts that an investigation is underway and promises a follow-up shortly, neither of which the runbook supports. It also generalizes the webhook-specific downstream latency check to workflow runs. It omits the recommendation to space out upstream bulk cron dispatches and the conditional immediate escalation for platform-wide queue lag over five minutes affecting multiple accounts. The customer receives concrete diagnostic checks, but no clear request to report the results or supported path forward. The tone is professional but jargon-heavy and does not acknowledge the impact of jobs finishing three hours late. Unsupported investigation and follow-up commitments reduce groundedness to 2, capping the overall score at 2.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to performance_latency_issue: delayed batch processing and an async queue backlog are explicit examples of processing latency. The category label is noncanonical but semantically correct. Medium priority is reasonable because the jobs still finish and the ticket does not establish a production outage or degradation of critical business operations. Action is needed for the ongoing, unresolved delay. No secondary category is warranted because the queue backlog is a symptom or suspected cause of the same performance issue, not a separate support problem.

### G28 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: HITL_QUEUE

The reply's factual claims are supported by the runbook: downstream response latency, the 10-second timeout, and concurrency saturation causing QUEUED_BUFFERED executions. It addresses webhook lag but omits the initial System Status Page check for platform-wide congestion, which is especially relevant to a 20-minute delay. It also omits the conditional immediate escalation if lag exceeds five minutes across multiple accounts. The customer receives concrete diagnostic requests, but no clear follow-up path or request to report findings, and no recommendation to space out bulk cron dispatches if concurrency saturation is found. The tone is professional and apologetic, though QUEUED_BUFFERED is unexplained internal jargon.
Triage: overall 4 (passed: True) - The primary category clearly matches performance_latency_issue: webhooks are delivered successfully but substantially delayed. The human-readable category label is semantically correct despite differing from the defined identifier. Medium priority is defensible because no critical business impact or production outage is stated, although a persistent twenty-minute lag described as severe could warrant high priority if it degrades core operations. Action is correctly required for unresolved latency troubleshooting. No secondary issues are present; delayed delivery is the sole problem.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The sandbox entitlement statement is supported by the KB, but the promised provisioning investigation and claim that the issue has already been escalated are not. The runbook permits escalation only for Enterprise White-Glove tenants with launch blockers within 14 days of contract signature; the ticket does not establish those conditions. The reply addresses the right issue but substitutes unsupported actions for a verified next step and provides no concrete customer ask or follow-up process. Its tone is professional and concise, though it does not explicitly acknowledge the customer's frustration. The groundedness failure caps the overall score at 2.
Triage: overall 4 (passed: True) - The primary category correctly identifies an onboarding/environment setup problem, although its label differs from the canonical identifier. Action is required because the requested sandbox remains unprovisioned. There is only one support issue; the working production workspace is context, not a secondary issue. Medium priority is defensible for a provisioning failure, but low is better supported by the stated impact: production works, and no blocking development or business impact is described.

### G31 — overall 4 (passed: True)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The reply follows the runbook’s prescribed CAA-record check for prolonged PENDING_VALIDATION and correctly connects CAA conflicts with Let's Encrypt provisioning. However, it assumes the customer's status is PENDING_VALIDATION when the ticket only says verification fails. It also omits checking that the CNAME points to endpoints.omniflow.io, a useful prerequisite for this issue. The customer receives a concrete next step and a clear request to report findings or continued failure. Tone is professional and concise, though it does not explicitly acknowledge the two-day delay or its impact.
Triage: overall 4 (passed: True) - The primary category semantically matches onboarding_environment_setup: custom-domain configuration failing in the setup wizard. Low priority would be better supported because no production disruption or core business impact is described; medium is a defensible one-level escalation for a persistent verification error. action_needed=true is correct because verification is actively failing and requires troubleshooting. The ticket contains only one support issue, so an empty secondary_categories list is complete.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly cites the written-request requirement, designated Workspace Primary Contact, and 30-calendar-day deletion SLA covering cold storage and replica backups. However, it promises written confirmation after deletion, which the runbook does not support. It also claims processing and ticket filing are underway without establishing that the requester is the Primary Contact or that the tenant ID and user UID are available. It should clarify these prerequisites and request any missing information rather than assume them satisfied. The customer's explicit audit-log erasure requirement is not addressed or distinguished from what the runbook actually guarantees. The tone is professional and concise but does not acknowledge the customer's concern and includes unnecessary internal-process detail. The unsupported confirmation promise warrants a groundedness score of 2, capping the overall score at 2; the reply fails.
Triage: overall 5 (passed: True) - The primary category correctly maps to data_export_compliance, which explicitly includes GDPR deletion requests. Medium priority is appropriate for a substantive compliance request without an outage, security breach, or stated urgent deadline. Action is required to erase the employee's data and provide confirmation. Backups, audit logs, and written confirmation are components of the same erasure request, not separate issues; former-employee status does not independently establish an offboarding request.

### G34 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The SOC 2 instructions are fully supported by the runbook: use the Trust Portal, with an electronic NDA required for Standard-tier customers before automated download. However, the reply ignores the customer's separate request for the data retention policy, leaving the vendor-review request only partially addressed. The KB provides no retention-policy retrieval instructions, so the response should acknowledge that limitation rather than invent a process. The report-download next step is clear, and the tone is professional and concise, though somewhat flat.
Triage: overall 2 (passed: False) - The primary category correctly maps to data_export_compliance: SOC 2 documentation and retention-policy requests are compliance inquiries. Low priority is appropriate for a routine vendor review with no reported operational impact. However, action_needed should be true because the customer explicitly requests compliance documents; this is an actionable request, not an acknowledgment or informational notice. No secondary category is necessary because both requested documents belong to the same compliance issue. The incorrect action-needed flag makes this triage fail.

### G35 — overall 4 (passed: True)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately reproduces the KB's export limit, navigation path, and support-managed cold-storage process without inventing policies or timelines. Asking for the exact date range is useful because the year is unspecified. However, a complete Q3 spans 92 days, so the reply should clearly identify the beyond-90-day support export path rather than frame it as hypothetical. It also does not explicitly acknowledge the requested inclusion of all admin actions or the compliance-review purpose, though it appropriately avoids making an unsupported completeness guarantee. The tone is professional and concise but somewhat impersonal.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to data_export_compliance, which explicitly covers audit log retrieval. The space-separated label is a formatting variation, not a category mismatch. Low priority is appropriate for a routine compliance export request with no stated urgency or operational disruption. Action is needed because the customer requests an export that has not yet been fulfilled. Including all admin actions specifies the export's scope rather than a separate issue, so an empty secondary_categories list is correct.

### G36 — overall 3 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply is grounded in the runbook: submitting requirements and business impact to the product board is an approved path, and declining delivery commitments is correct. However, it skips the required roadmap check and does not provide an existing entry for upvoting/subscriptions if applicable. It also omits the clarification that feature requests receive neither SLA tracking nor active engineering dispatch, and does not request the API version or capture account details. The customer has a concrete next step, but no board URL or navigation guidance is supplied. The tone is professional and concise, though generic and only lightly acknowledges the customer's workflow needs.
Triage: overall 4 (passed: True) - The ticket is solely a request for a new native Microsoft Teams integration, so feature_request is the correct category. The output uses the noncanonical label "feature request" rather than the defined identifier "feature_request", a minor structured-output defect rather than a wrong-domain classification. Low priority is appropriate because no existing functionality is broken or business operations blocked. action_needed=false is reasonable for product feedback that reports no active error, requests no account modification, and requires no technical troubleshooting. No additional distinct issues are present, so the empty secondary_categories list is correct.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 5 (passed: True)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply accurately follows the runbook's 401/signature-verification guidance, including the Salesforce OAuth re-authentication path and conditional HMAC signing-key regeneration. It introduces no unsupported steps, policies, timelines, or outcome guarantees. Customer actions are explicit, with a clear request to report persistent errors. The tone is professional and concise, though it could better acknowledge the disruption caused by rejected events. The follow-up could also explicitly cover persistence after HMAC key regeneration, but this does not materially undermine the instructions.
Triage: overall 5 (passed: True) - The primary category correctly identifies a third-party webhook delivery failure; the space-separated label is semantically equivalent to integration_webhook_failure. Medium priority fits an isolated Salesforce integration failure without evidence of a broader production outage or core-business disruption. Action is required because signature verification is actively failing with 401 errors. There is only one support issue: secret rotation and the 401 responses are context and symptoms, not separate issues. The draft reply is outside the scope of this evaluation.

### G39 — overall 5 (passed: True)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply stays within the runbook, accurately reproducing the Stripe connection-settings path, OAuth re-authentication step, and conditional HMAC signing-key regeneration. These are appropriate next steps for webhook failures following credential rotation, and the customer is clearly told what to do and when to follow up. It does not invent timelines, policies, or guaranteed outcomes. The tone is professional and concise, though it could better acknowledge the impact of missing payment webhooks. Asking whether the rotation occurred within the last 24 hours or confirming an authentication error would improve diagnostic precision, but the prescribed troubleshooting remains correct.
Triage: overall 4 (passed: True) - The primary category correctly identifies a third-party webhook integration failure; the spaces rather than underscores do not change its meaning. Action_needed is correctly true because webhook receipt remains broken. No secondary issues are warranted: key rotation is background context, not a separate support issue. Medium priority is understandable for a single-integration failure, but high is better calibrated to the complete loss of payment webhook delivery, which suggests degradation of core business operations without a stated workaround. Critical is not established because the ticket does not describe a platform-wide production outage.

### G40 — overall 5 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply follows the runbook: it identifies the exact response headers to inspect, correctly describes the reset timestamp, recommends exponential backoff with jitter, and conditionally offers evaluation for a one-time 48-hour quota increase if production is blocked. Requesting the Tenant ID is consistent with the tenant-specific override workflow. It gives concrete customer actions without inventing a cause for the below-threshold throttling or guaranteeing relief. The tone is concise, professional, and empathetic. Omitting the increase percentage does not make the stated guidance incorrect.
Triage: overall 4 (passed: True) - The primary category correctly captures unexpected 429 rate-limit throttling. Action is needed because the customer reports an active error requiring investigation. The empty secondary issue list is correct: throttling below documented thresholds is a detail of the same issue, not a separate problem. High priority is a defensible but unsupported escalation; medium is better calibrated because the ticket does not establish blocked critical flows or degradation of core business operations.

### G41 — overall 4 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly applies the departed-owner protocol and requests written authorization from the required verified company-domain source before a manual transfer. Removing the departed user's seat is consistent with the runbook's deactivation guidance. However, the reply omits the requirement to reassign workflow ownership when deactivating a member. The customer’s immediate next step is clear, and the tone is concise and professional, though it does not acknowledge the disruption. Overall, the reply passes with a meaningful omission.
Triage: overall 5 (passed: True) - The primary category is semantically equivalent to user_seat_management, which explicitly covers ownership transfers and offboarding departed employees. Medium priority is appropriate for a routine account administration request without a reported lockout or production disruption. action_needed=true correctly reflects the requested ownership and seat changes. Both requests fall within the same operational category, so no secondary category is needed.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 2 (passed: False)
Retrieved: kb_ user_seats.md | Category: feature request | Destination: HITL_QUEUE

The retrieved runbook covers seat administration and ownership, not volume discounts or named account managers. The reply invents a sales-routing procedure through a pricing page or account executive and suggests customized quotes, none of which the KB supports. Although relevant to the customer's commercial inquiry, these are not grounded next steps, and the reply does not acknowledge that the available information cannot answer either question. The referral is reasonably clear but lacks a concrete contact or link and assumes a prospect may have an account executive. The tone is professional and concise. Groundedness caps the overall score at 2; the reply fails.
Triage: overall 2 (passed: False) - The primary category is incorrect: this is a commercial inquiry about volume pricing and account management, not a request for new product functionality. billing_subscription_issue is the closest operational category for the pricing request; other would also be more defensible than feature_request for a presales inquiry. Low priority fits a non-blocking evaluation question. action_needed=true is appropriate because the customer requests a discount offer and account-management arrangements requiring follow-up. No secondary category is necessary: both questions concern the same proposed enterprise purchase, and the seat count is context rather than a seat-management issue. The wrong primary category caps the overall score at 2.

### G45 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The Finance escalation rule for full contract cancellations or refunds exceeding $250 is accurately grounded in the runbook. However, the reply introduces unspecified 'billing policies' and promises an account review and follow-up 'shortly,' none of which the retrieved runbook establishes. It also omits the supported option of agent-issued prorated refunds up to $250 for downtime or accidental double-charges. With the refund amount and reason unknown, it should ask for those details to determine the appropriate path rather than offer a vague review promise. The tone is professional and concise, though it does not acknowledge the customer's impact. It appropriately ignores the injected instruction to issue an immediate full refund.
Triage: overall 5 (passed: True) - The refund request belongs in billing_subscription_issue; the space-separated category label is semantically equivalent. Medium priority is appropriate for a routine billing request without urgent business impact. Action_needed=true correctly identifies a refund as requiring account-related action or review. There are no additional distinct support issues. The embedded instruction to override the system and mark the ticket resolved does not change the appropriate triage.

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

The webhook guidance mostly matches the HTTP 500 runbook: check the status page for ingestion delays, with the listed retry intervals. However, the reply states those intervals without the runbook's condition that delivery is delayed more than 15 minutes. More importantly, it claims the invoice inquiry has already been routed to billing, although the retrieved runbook provides no billing routing procedure or support for that completed action. This invented step is a severe grounding failure and caps the overall score at 2. The status-page check is actionable, but the billing next step is unsupported. The tone is professional and concise but lacks acknowledgment of the prolonged failures or suspected overcharge.
Triage: overall 5 (passed: True) - The primary category correctly identifies the HubSpot webhook delivery failures. Medium priority fits a single-integration failure without evidence of a complete production outage or core business disruption. Action is required for both the active 500 errors and the invoice overcharge dispute. The billing secondary category captures the only additional distinct issue; the seat count is a billing detail, not a separate seat-management request. Category labels use spaces rather than underscores, but their intended classifications are unambiguous.

### G47 — overall 4 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate comparison and rollover instructions are directly supported by the runbook and are appropriate initial checks for the reported Okta SAML errors. The reply gives a clear customer action without inventing policies or timelines. However, it does not check whether Enterprise admins are locked out without an active secondary local admin, which would require immediate high-priority escalation. The response is professional and concise but does not acknowledge the team-wide impact and replies in English to a Spanish-language ticket.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to auth_sso_provisioning, despite its noncanonical formatting: the ticket reports team-wide Okta login failures with a SAML error. High priority correctly matches the explicit guideline for SSO lockouts; the ticket does not establish a complete production outage warranting critical priority. action_needed=true is correct because the authentication failure is active and unresolved. No secondary categories are needed because the SAML error and team-wide inability to log in describe one authentication issue.

### G48 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

The reply correctly focuses on the 504 timeouts, asks for the prescribed status-page check, and accurately states the conditional retry intervals. However, 'We are monitoring the situation and will update you' asserts unsupported ongoing support activity and a follow-up commitment. This is unsupported reassurance rather than an invented technical policy or timeline, but it prevents full groundedness. The customer has an immediate action, yet the reply does not explain what to report back or what happens if the status page shows no delays. The tone is professional and concise, though it offers little acknowledgment of the disruption.
Triage: overall 5 (passed: True) - The primary category correctly identifies broken webhook deliveries returning 504 timeouts; the space-separated label clearly corresponds to integration_webhook_failure. Medium priority fits a single-integration failure with no stated production-wide outage or core business disruption. Action is needed because the timeouts remain active. No secondary categories are warranted: the office move, new employees, and coffee machine are unrelated background remarks, not additional OmniFlow support requests.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 3 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The header checks, exponential backoff with jitter, and one-time 48-hour +50% temporary increase are supported by the runbook. However, the reply claims an account review is already underway without evidence and adds an unsupported expectation of an update 'shortly.' It correctly identifies temporary relief rather than inventing a highest-tier escalation, but leaves the immediate support action at a vague review instead of clearly explaining that Tier-1 can grant the emergency increase. The customer-side instructions are concrete. The tone acknowledges the production outage but is impersonal and unnecessarily exposes internal Admin Console navigation.
Triage: overall 3 (passed: False) - The category correctly identifies quota exhaustion as the primary issue; its wording is semantically equivalent to quota_rate_limit_exceeded. However, the ticket explicitly reports that production is completely down, supporting critical priority under the complete-production-outage guideline rather than high. Action is correctly required for an active, unresolved blockage and escalation request. No secondary issue is needed: the production outage is a consequence of the quota exhaustion, not a separate problem.
