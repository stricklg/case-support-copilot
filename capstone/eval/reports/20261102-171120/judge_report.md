# Capstone eval report

Run at: 2026-11-02T17:17:27.938995+00:00 (mode: replay)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 86.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 3.42
- Avg accuracy: 3.42
- Avg actionability: 3.52
- Avg tone: 3.88
- Avg overall: 3.03
- Pass rate (overall = 5): 0.182
- Pass rate (overall >= 4): 0.364

## Judge (triage decisions)
- Cases judged: 33
- Avg t_category_fit: 4.76
- Avg t_priority_calibration: 4.64
- Avg t_action_needed: 4.76
- Avg t_issue_completeness: 4.94
- Avg t_overall: 4.3
- Pass rate (overall >= 4): 0.848
- Pass rate (overall = 5): 0.576

## Costs
Prices as of 2026-11-02 (USD); token counts measured, not estimated.
- Judge (measured live): $0.2868
- replay mode: generator and embedding calls are not re-run, so their costs are not measured; judge costs above are measured live

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 4 (passed: True)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly applies the HTTP 500/504 guidance: checking the status page for ingestion pipeline delays and conditionally describing the exact retry intervals when delivery is delayed more than 15 minutes. It introduces no unsupported policy or timeline. The next step is concrete, but the follow-up request ('if the issue persists') is vague and does not ask the customer to report the status-page findings or delivery-delay duration. The tone is professional and concise, though it does not explicitly acknowledge the impact of failed contact-create events. The conditional escalation criteria are not established by the ticket, so omitting them is appropriate.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to integration_webhook_failure despite using spaces instead of underscores: the ticket reports HubSpot webhook delivery failures with HTTP 500 responses. Medium priority is appropriate for a single-integration error with no stated widespread outage or critical business impact. Action_needed is correctly true because the error is active and unresolved. No additional distinct issues are reported, so the empty secondary_categories list is correct. The draft reply is outside the evaluation scope.

### G07 — overall 4 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply correctly recommends monitoring the three specified headers and implementing exponential backoff with jitter. Its conditional offer to evaluate 48-hour temporary relief is consistent with the runbook and does not guarantee approval. Asking for a Tenant ID is a reasonable operational clarification given the tenant-specific override, though not explicitly prescribed as a customer action. Minor omissions include explaining that X-RateLimit-Reset uses Unix epoch seconds and stating that relief is a one-time +50% increase. 'Completely blocked' slightly narrows the runbook's eligibility wording. The reply provides concrete next steps and is concise and professional, but acknowledges the issue without explicitly expressing empathy for the disrupted sync. Overall, it passes with minor shortcomings.
Triage: overall 5 (passed: True) - The primary category clearly matches the reported API 429 rate limits, despite using a human-readable label rather than the canonical identifier. Medium priority is appropriate for an isolated nightly batch-sync issue with no stated critical-flow blockage or broader production outage. Action is required because the customer reports an active error. The ticket contains only one distinct issue, so an empty secondary_categories list is correct.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply directly addresses purchasing 20 additional seats and gives the exact purchase path supported by the runbook: Billing > Manage Seats. It clearly states the customer's next action without inventing policies, timelines, or outcomes. The tone is concise, professional, and appropriate for a straightforward purchase request.
Triage: overall 4 (passed: True) - User seat management is a defensible category for expanding workspace seats, although purchasing licenses also overlaps with billing_subscription_issue. The category label should use the defined identifier user_seat_management rather than 'user/seat management'. Low priority is defensible because no outage or blocked users are reported, though medium would better align with the commercial account-update aspect. Action is correctly required for the requested account modification. The ticket contains only one issue, so the empty secondary category list is correct.

### G09 — overall 4 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

All configuration details are supported by the runbook, and the reply appropriately makes the JIT requirements conditional. However, the certificate check comes from signature-mismatch troubleshooting and does not directly explain configuring assertions for a new subdomain. The reply gives concrete checks but does not acknowledge that the KB lacks subdomain-specific setup instructions or ask a targeted question to clarify the customer's setup and provisioning needs. The tone is professional and concise, though somewhat impersonal. No unsupported steps, policies, timelines, or outcome promises are introduced.
Triage: overall 5 (passed: True) - The primary category correctly maps to auth_sso_provisioning because the request concerns Okta SAML configuration. Low priority is appropriate for setup assistance with no reported login failure, lockout, or production impact. Action is needed because the customer explicitly requests help with unresolved configuration. No secondary category is warranted: the new subdomain is context for the SSO setup, not a separate reported routing or onboarding issue.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The CSV export navigation is supported, but the KB describes security and activity log exports, not raw audit log table exports generally. It does not establish that Parquet is unavailable or authorize a product-request workflow. Claiming the request has been logged for product review invents a completed action and next step. The reply also omits the Workspace Admin requirement and 90-day limit for CSV exports. Although polite and concise, it does not provide a grounded next step for the requested enhancement. The groundedness failure caps the overall score at 2.
Triage: overall 2 (passed: False) - The ticket requests a new export format, so feature_request is the best category rather than data_export_compliance. Low priority is appropriate, and there are no additional distinct issues. However, action_needed should be true: the customer explicitly asks for a product change that requires product-team review or escalation, rather than sending an acknowledgment or informational message. The false flag incorrectly treats an actionable feature request as requiring no action.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 5 (passed: True)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply accurately follows the card-declined runbook: it directs the customer to the correct payment-method settings, then to Retry Pending Invoice for an immediate retry, and correctly states the 7-day grace period. It clearly identifies the customer's next actions without claiming support has retried the charge. The tone is professional and concise, though the greeting is flat, it does not acknowledge the inconvenience, and 'tenant suspension' is internal jargon.
Triage: overall 5 (passed: True) - The primary category correctly identifies a billing subscription issue, despite using spaces rather than the defined underscore-separated label. Medium priority matches a failed invoice payment without a reported suspension or operational outage. Action is needed because the customer explicitly requests a charge retry. The failed payment warning is a symptom of the declined payment, not a separate issue, so the empty secondary category list is correct. The draft reply is outside the scope of this evaluation.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply correctly cites support’s authority to issue prorated refunds for accidental double-charges up to $250 without manager approval. However, it claims an account review is underway and implies the refund will be processed, neither of which is established by the KB or ticket. The refund amount is unknown, so it cannot assume support can process it directly; requests exceeding $250 require Finance escalation. The reply offers a concrete-sounding next step but does not clarify this conditional routing or request information needed to determine it. The tone is professional and concise, though it offers little acknowledgment of the financial impact. The unsupported operational claim and premature refund commitment cap the overall score at 2.
Triage: overall 5 (passed: True) - The primary category clearly matches a subscription billing dispute, despite using spaces rather than underscores in the category label. Medium priority is appropriate for a duplicate charge with no stated operational outage or urgent impact. Action is required to investigate and refund the duplicate payment. The ticket contains one distinct billing issue, so no secondary categories are needed. The draft reply is outside the scope of this evaluation.

### G17 — not judged (status 200, destination HITL_QUEUE)

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply presents the billing settings path as a supported way to switch to ACH, but the runbook prescribes that path only for updating a billing card after a declined payment. Although ACH is listed in scope, no ACH-switching procedure or scheduling guidance is provided. The reply therefore invents applicability of a step to this issue and does not address the requested start next month. It gives a concrete navigation step, but not a grounded next step for the actual request. The tone is professional and concise, though generic. The groundedness failure caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category correctly identifies a billing payment-method change; the space-separated label is semantically equivalent to billing_subscription_issue. Medium priority matches the guideline for billing update inquiries. Action is required because the customer requests an account billing modification. There is only one distinct issue, so an empty secondary_categories list is correct. The draft reply is outside the scope of this evaluation.

### G20 — overall 4 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply's certificate verification and PEM rollover guidance are directly supported by the runbook and address the likely SAML signature issue following the metadata update. It gives a clear customer action and requests follow-up if the problem persists. However, because all users are affected, it should clarify whether Enterprise admins are locked out without a secondary local admin, which would require immediate high-priority escalation. The tone is professional and concise but does not acknowledge the impact of the organization-wide login failure.
Triage: overall 5 (passed: True) - The primary category clearly maps to auth_sso_provisioning: all users experience an Okta SAML authentication failure. High priority matches the explicit guideline for SSO lockouts; no complete production processing outage or security breach is reported to justify critical. Action is required because the authentication error is active and unresolved. No secondary issue is present: the metadata update is troubleshooting context, not a separate support request. The category uses a formatting variant of the defined label but unambiguously identifies the correct category.

### G21 — overall 5 (passed: True)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately reproduces all three SCIM troubleshooting checks in the runbook: bearer-token expiration and its 180-day validity, exact case-sensitive email matching, and available unassigned seats. It directly addresses the provisioning issue and clearly asks the customer to perform these checks without inventing policies, timelines, or outcomes. The tone is professional and concise, though it does not explicitly acknowledge the impact on new hires. That minor tone weakness does not materially detract from an otherwise fully grounded and actionable reply.
Triage: overall 4 (passed: True) - The primary category correctly maps to auth_sso_provisioning: failed Okta SCIM provisioning is explicitly within its scope. Action is needed because automatic provisioning remains broken, even though the sync reports no errors. There is only one distinct issue, so no secondary categories are needed. Medium priority is defensible because no production outage or explicit login lockout is reported, though high would better reflect provisioning failures affecting multiple new employees and potentially blocking access.

### G22 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The reply introduces an unsupported setup prerequisite—ensuring a separate workspace environment—and presents assertion mapping as a general SSO configuration step, whereas the runbook only specifies assertions for JIT provisioning. The certificate check and settings path are supported, but they are troubleshooting guidance for signature errors, not instructions for configuring Entra ID for a second workspace. The reply does not provide a supported setup path or clearly ask for information needed to determine the next step; asking the customer to report hypothetical errors does not resolve the request. The tone is professional and concise, though it offers little acknowledgment of the customer's goal. The supplied runbook does not cover second-workspace setup, and the reply should acknowledge that limitation rather than infer setup requirements. Groundedness caps the overall score at 2.
Triage: overall 2 (passed: False) - The primary issue is configuring Microsoft Entra ID SSO, which belongs in auth_sso_provisioning. The new European workspace is context, not a separate environment-setup support issue. Listing SSO as secondary does not correct the wrong primary category and unnecessarily splits one request into two issues. Low priority is appropriate for non-blocking initial configuration with no reported authentication failure, and action_needed=true is correct for an actionable SSO configuration request. The wrong primary category caps the overall score at 2.

### G23 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate comparison and required JIT attributes are supported by the KB, but only for signature errors and failed account creation, respectively. The KB does not identify either as a redirect-loop remedy, so presenting them as troubleshooting steps for this ticket is not adequately grounded. The reply also invents escalation to a technical team if the issue persists; the only documented escalation is immediate, HIGH-priority escalation to security support for Enterprise admin lockouts with no active secondary local admin. The reply gives concrete checks and a follow-up request, but they are not established next steps for this issue. Its tone is professional, empathetic, and concise. The groundedness score caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category clearly maps to auth_sso_provisioning despite its differently formatted label. A Google Workspace SSO redirect loop is an authentication failure, so high priority is appropriate. The active login error requires troubleshooting, making action_needed=true correct. The ticket contains only one support issue, so an empty secondary_categories list is complete.

### G24 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The navigation path and Sanitize / Coerce Node recommendation are explicitly in the KB, but only for schema validation failures caused by strict typing. The reply extends these remedies to a branch-condition syntax error without evidence that schema validation or field typing is the cause. It therefore does not establish an appropriate next step for the customer's actual issue. The KB contains no guidance on string-comparison syntax; the reply should acknowledge that limitation rather than conflate syntax and schema errors. The instructions are concrete and the tone is polite and concise, but the reply does not acknowledge the impact of the failed workflow.
Triage: overall 5 (passed: True) - The primary category clearly matches a branch-condition syntax error, despite using a human-readable label rather than the category's underscore identifier. Medium priority is appropriate for an isolated workflow failure with no reported broader production impact. The active unresolved error correctly requires action. Only one distinct issue is reported, so empty secondary categories are correct. The draft reply is outside the scope of this evaluation.

### G25 — overall 5 (passed: True)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply accurately follows the KB's schema-validation guidance: strict typing as a potential cause, the exact Raw Input diagnostic path, and a Sanitize / Coerce Node before branch evaluation. It provides concrete customer actions without inventing a policy, timeline, or guaranteed outcome. The generic invitation to follow up does not introduce an unsupported escalation procedure. Tone is professional and concise, though somewhat formulaic and lacking explicit acknowledgment of the frustration caused by a payload that validates externally.
Triage: overall 5 (passed: True) - The primary category clearly matches a JSON schema validation error within a transform step, despite using a human-readable label rather than the canonical category identifier. Medium priority is appropriate for an isolated workflow error with no reported broader outage or critical business impact. The active, unresolved error correctly requires action. No secondary categories are needed because external validation is context for the same issue, not a separate support problem.

### G26 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms limit, backtracking protection, and regex optimization advice are directly supported by the runbook. However, the customer reports non-matching results, not timeouts, and the reply applies timeout-specific guidance without establishing that a timeout occurred. The retrieved runbook does not explain ordinary regex non-matches; the reply should acknowledge that limitation rather than assume the timeout scenario. The suggested edits and follow-up request are concrete but may not address the actual issue. The tone is professional and concise, but lacks acknowledgment of the customer's difficulty.
Triage: overall 4 (passed: True) - The primary category correctly identifies a regex failure within a workflow, matching workflow_syntax_execution_error despite the label formatting difference. Priority should be medium rather than low: the customer reports an active, isolated workflow error, not a general inquiry or cosmetic issue. action_needed=true is correct because troubleshooting is required. The empty secondary_categories list is appropriate because only one distinct issue is reported. The draft reply is not part of this evaluation.

### G27 — overall 2 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The concurrency limits and QUEUED_BUFFERED state are supported by the runbook. However, 'We are looking into your case' and the promise of updates 'shortly' assert an investigation and update timing not supported by the KB. The reply also omits the first diagnostic step—checking the System Status Page—and the recommended mitigation of spacing upstream bulk cron dispatches. It asks about downstream backpressure without establishing the runbook's condition of high webhook dispatch latency. Customer checks are concrete, but the subsequent troubleshooting path is incomplete. The tone is polite, but jargon-heavy and does not acknowledge the impact of jobs finishing three hours late. The groundedness score caps the overall score at 2.
Triage: overall 4 (passed: True) - The primary category correctly identifies a performance/latency issue: delayed batch processing and an async queue backlog directly match the category definition. The label uses different formatting from the canonical category name but has the correct meaning. Medium priority is defensible because no outage or explicit critical-business impact is reported, although recurring three-hour delays could warrant high priority as operational degradation. Action_needed is correctly true for an unresolved performance problem. No secondary categories are needed because the queue backlog is part of the same issue, not a separate support request.

### G28 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: HITL_QUEUE

The diagnostic advice, thread limits, QUEUED_BUFFERED state, and 10-second timeout are supported by the runbook. However, the claim that the team is reviewing the ticket for escalation is unsupported. The reply correctly addresses delivery latency but omits spacing out upstream bulk cron dispatches if concurrency is saturated. It also fails to explain that platform-wide lag over five minutes affecting multiple accounts requires immediate escalation; the reported twenty-minute delay alone does not establish that condition. Customer checks are clear, but the reply does not ask the customer to report their findings or provide a concrete conditional next step. The tone is professional and empathetic, though QUEUED_BUFFERED is unexplained internal jargon.
Triage: overall 4 (passed: True) - The primary category correctly corresponds to performance_latency_issue: webhooks are delivered successfully but substantially delayed, rather than failing. Medium priority is defensible because no production outage or explicit business-critical impact is reported, although the severe twenty-minute delay could warrant high priority if core operations are affected. Action is needed for the ongoing latency problem. Empty secondary_categories is correct because the ticket describes only one issue.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The statement that Pro and Enterprise accounts include an isolated sandbox is supported. However, the reply invents a support escalation and tenant-provisioning verification procedure, neither of which the runbook prescribes. The only documented escalation applies to Enterprise White-Glove tenants with launch blockers within 14 days of contract signature; the ticket does not establish that eligibility. The promise to follow up 'shortly' is also unsupported. The response addresses the sandbox issue and names a concrete next action, but that action is not grounded in the runbook. Its tone is professional and concise, though it does not explicitly acknowledge the customer's delay or impact. The groundedness failure caps the overall score at 2.
Triage: overall 4 (passed: True) - The primary category correctly identifies an onboarding/environment setup issue, despite using a display-style label rather than the defined enum. Action is needed because the sandbox remains unprovisioned and requires investigation. There is only one distinct issue; the working production workspace is context, not a secondary issue. Medium priority is defensible for an unresolved provisioning failure, though low is the closer fit given that production works and no blocking business impact is described.

### G31 — overall 3 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The CAA-record check is supported for PENDING_VALIDATION lasting more than two hours, but the reply assumes that specific status without confirmation: the customer only reported failed verification. It should confirm the status and ask the customer to verify that the CNAME points to endpoints.omniflow.io. The customer has a clear immediate action and follow-up instruction, though further investigation is not specified in the runbook. The tone is professional and concise, but does not acknowledge the impact of the two-day delay. Overall, the reply does not pass.
Triage: overall 4 (passed: True) - The primary category semantically matches onboarding_environment_setup exactly: custom domain configuration and verification belong there. Action is required because verification is actively failing. The empty secondary issue list correctly captures a single problem; the CNAME record and setup wizard failure are details of that problem. Medium priority is defensible for a persistent setup error, but low would be better calibrated without evidence of production impact or blocked core operations. The draft reply was not considered.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly cites the written-request requirement for the designated Workspace Primary Contact and the 30-calendar-day deletion SLA covering backups. However, it claims the request has already been initiated without evidence and invents a registered-email or verification requirement not present in the runbook. It also omits the prescribed internal DPO ticket with tenant ID and user UID. Although it gives the customer an action, that action is partly unsupported. The customer's concerns about audit logs and written confirmation remain unaddressed; the KB does not establish a confirmation procedure or explicitly resolve audit-log deletion, so these should not be promised. The tone is professional but lacks acknowledgment of the customer's concern and uses internal jargon ('DPO processing'). The groundedness failure caps the overall score at 2.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to data_export_compliance, which explicitly covers GDPR deletion requests. Medium priority is appropriate for an actionable compliance request without a stated urgent deadline, outage, or security breach. action_needed=true is correct because the customer requests data erasure and written confirmation. Backups, audit logs, and confirmation are components of the same erasure request, not separate issues; the former employee reference does not establish a distinct offboarding request.

### G34 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The SOC 2 guidance is fully supported by the runbook: it directs the customer to the correct Trust Portal and correctly identifies the electronic NDA requirement for Standard-tier customers. However, the reply ignores the customer's separate request for the data retention policy, leaving that part of the vendor review unresolved with no next step. The KB provides no procedure for obtaining that policy, so the reply should acknowledge the limitation rather than invent instructions. The tone is professional and concise but offers little acknowledgment of the customer's audit needs.
Triage: overall 2 (passed: False) - The primary category correctly corresponds to data_export_compliance: SOC 2 documentation and retention-policy inquiries belong in that category. Low priority is appropriate for a routine vendor-review request with no operational disruption. However, action_needed should be true: the auditors' requested documents still need to be provided or made accessible, so this is an actionable request, not an acknowledgment or informational notice. No secondary category is necessary because both requested documents fall within the same compliance issue.

### G35 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The self-service navigation, 90-day export limit, and support-generated cold-storage query are supported by the runbook. Asking the customer to confirm Enterprise status is a reasonable clarification, although the runbook does not explicitly require that verification. The main issue is that Q3 spans 92 days, so the reply should recognize that the complete requested export exceeds the self-service limit and explicitly identify the support-generated archive query as the next step, rather than presenting it only conditionally. The customer is given a concrete question, but the route to fulfilling the full-quarter request remains insufficiently clear. The tone is professional and concise, though it does not acknowledge the compliance-review purpose.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to data_export_compliance despite using spaces instead of underscores: the sole request is a complete Q3 audit-log export, including admin actions. Low priority fits a routine compliance request with no reported outage, blocker, or urgency. Action_needed=true is correct because the customer requests an export requiring action. No additional distinct issues are present, so an empty secondary_categories list is appropriate.

### G36 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply correctly avoids delivery commitments and gives a concrete submission step. However, the KB does not establish that all feedback is tracked through the public roadmap or that upvotes influence prioritization; those are unsupported process claims. It also skips the prescribed roadmap check and does not provide an existing entry URL if available. The request for workflow details is useful but omits the other required information, and the reply does not clarify that feature requests receive neither SLA tracking nor active engineering dispatch. The tone is polite and concise, although it does not specifically acknowledge the team's reliance on Teams. The groundedness score caps the overall score at 2.
Triage: overall 5 (passed: True) - The ticket is a straightforward request for a new native Microsoft Teams integration, so feature_request is the best category. The output's 'feature request' label is semantically equivalent, although it does not use the exact defined identifier. Low priority is appropriate because no existing functionality is broken or business operations blocked. action_needed=false is appropriate for a product suggestion that requires neither account modification nor technical troubleshooting. There are no additional distinct support issues.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 5 (passed: True)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply follows the runbook's 401 guidance: re-authenticate Salesforce via OAuth and, if using HMAC verification, regenerate the signing key at the specified location. It provides concrete customer actions without inventing policies, timelines, or troubleshooting steps. The tone is professional and concise, though it does not explicitly acknowledge the impact of rejected events. Asking whether the rotation occurred within 24 hours would improve diagnostic completeness, but the customer has already identified secret rotation as the trigger.
Triage: overall 5 (passed: True) - The primary category clearly maps to integration_webhook_failure despite using spaces instead of underscores: Salesforce webhook signature failures and rejected deliveries are integration failures. Medium priority fits an isolated integration failure with no stated broader production outage or critical business impact. Action is required because the customer reports ongoing 401 errors. There is only one distinct issue; secret rotation and signature verification errors are context and details of that issue, so no secondary categories are needed. The draft reply is outside the scope of this evaluation.

### G39 — overall 4 (passed: True)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply gives the exact OAuth re-authentication path and conditional HMAC signing-key regeneration step prescribed by the runbook, without inventing policies, timelines, or outcomes. It addresses the reported post-rotation webhook failure and provides clear customer actions. However, it skips verifying whether the signing secret or OAuth token changed within the last 24 hours and does not establish whether the failure involves 401 responses or expired signatures before selecting that diagnostic branch. The tone is professional and concise but does not acknowledge the disruption to payment webhooks. Overall, it passes with minor diagnostic and empathy omissions.
Triage: overall 4 (passed: True) - The primary category correctly identifies a third-party webhook delivery failure. Medium priority is defensible for a single-integration failure, but high would better reflect the complete loss of payment webhook delivery and its likely impact on core business operations. Critical is not established because the ticket does not describe a platform-wide production outage. Action_needed is correctly true for an active, unresolved error. There is only one distinct issue; key rotation is its background trigger, not a separate support issue, so the empty secondary_categories list is correct.

### G40 — overall 5 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply follows the runbook: it asks the customer to inspect the three specified rate-limit headers, recommends exponential backoff with jitter for 429 responses, and conditionally offers evaluation of temporary relief if production is blocked. Requesting the Tenant ID is consistent with the tenant-specific override workflow. It does not invent a reason for throttling below documented thresholds or promise an unsupported resolution. The customer’s next steps are clear, and the tone is concise, professional, and empathetic. Omitting the override’s duration and percentage is not material because the reply only offers to evaluate eligibility.
Triage: overall 5 (passed: True) - The primary category clearly matches the reported 429 rate-limit throttling, despite using a human-readable label rather than the canonical category identifier. Medium priority is appropriate because the ticket does not establish a production outage, critical-flow blockage, or significant business degradation. Action is needed to investigate the active throttling below documented thresholds. There is only one distinct support issue, so an empty secondary_categories list is correct.

### G41 — overall 4 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly follows the departed-owner protocol and requests the required written authorization from an appropriate verified company-domain email. Transferring ownership and removing the former owner's access are supported by the runbook, with no invented timeline or policy. However, it omits the requirement to reassign workflow ownership when deactivating the former member. The next step is clear, but the tone is somewhat flat and the internal label 'Departed Owner Protocol' is unnecessary.
Triage: overall 4 (passed: True) - The primary category clearly corresponds to user_seat_management, which explicitly covers ownership transfers and offboarding departed employees, although the output uses a noncanonical label. Action is required because the customer requests ownership and seat changes. These requests form one coherent offboarding issue, so no secondary category is needed. Medium priority is defensible for an administrative account change, but low is better supported because no lockout, operational disruption, or urgency is reported.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 1 (passed: False)
Retrieved: kb_ user_seats.md | Category: feature request | Destination: HITL_QUEUE

The retrieved runbook covers seat allocation, ownership transfers, and workspace mergers—not volume discounts or named account managers. The reply invents a sales follow-up, custom plans, pricing tiers, and a 'shortly' timeline, none of which is supported. It acknowledges the customer's inquiry but neither answers it with grounded information nor provides a supported next step. The promised outreach sounds actionable but has no basis in the KB. The tone is professional and concise, though generic. The response should instead acknowledge that the available documentation does not establish discounts or named account manager availability, without promising unsupported outreach.
Triage: overall 2 (passed: False) - The primary category is incorrect: volume pricing and named account management are commercial sales inquiries, not requests for new product functionality. Given the definitions, 'other' is the best fit for this prospective enterprise-sales inquiry; billing_subscription_issue is a closer alternative than feature_request. Low priority is appropriate because no operational disruption is reported. Action is needed because the requested pricing offer and account-management arrangement require a sales response. The two questions form one enterprise-sales inquiry, so no secondary category is necessary. The wrong primary category caps the overall score at 2.

### G45 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The Finance escalation rule is correctly quoted, and the reply appropriately ignores the injected demand for an immediate full refund. However, the promise that an agent will review the account 'shortly' introduces an unsupported action and timeline. The reply also does not establish whether escalation is actually needed, request the refund amount or reason, or explain the runbook's prorated-refund option for downtime or accidental double-charges up to $250. Its tone is professional and concise, though minimally empathetic. The groundedness failure caps the overall score at 2.
Triage: overall 5 (passed: True) - The refund request is a billing/subscription issue, and medium priority is appropriate for a routine financial account request without urgent business impact. Action_needed=true correctly reflects an actionable refund request; the embedded instruction to mark it resolved does not establish resolution. No additional distinct support issues are present, so an empty secondary_categories list is correct. The category's space-separated wording clearly identifies the intended category. Draft-reply claims are outside the scope of this evaluation.

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

The retry intervals and status-page check are supported by the runbook for HTTP 500 errors, but retries are presented unconditionally rather than in the context of delivery delays exceeding 15 minutes. More importantly, the reply claims the support team has been notified to review the billing issue, although the KB provides no billing workflow and nothing establishes that notification occurred. This invented action is a severe grounding failure and caps the overall score at 2. The webhook guidance is relevant and actionable, but the invoice next step is unsupported. The tone is professional and concise, though it does not acknowledge the impact of the prolonged webhook failures.
Triage: overall 5 (passed: True) - The primary category correctly identifies the HubSpot webhook delivery failures. Medium priority is appropriate for a single-integration failure with no stated production-wide outage or core-business disruption. Action is needed for both the active 500 errors and the disputed invoice charge. The secondary billing category captures the separate seat-overcharge issue without adding phantom issues. The space-separated category labels are semantically equivalent to the defined categories.

### G47 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate comparison and PEM upload guidance are supported by the runbook and relevant to the team's Okta SAML error. However, the claim that support is monitoring the issue and will restore access promptly is unsupported: the runbook establishes neither active monitoring nor a restoration timeline. This caps the overall score at 2. The rollover instructions also omit the required sequencing: upload the new certificate before switching the primary certificate in the IdP. The reply provides a concrete initial check but does not explain what to report if it fails or check whether the admin-lockout escalation condition applies. Its tone is professional and acknowledges the impact, but replying in English to a Spanish ticket reduces its customer suitability.
Triage: overall 5 (passed: True) - The primary category clearly corresponds to auth_sso_provisioning despite its formatting variation: the entire team is unable to log in through Okta due to a SAML error. High priority is explicitly appropriate for SSO lockouts; the ticket does not establish a complete production outage warranting critical priority. action_needed=true correctly reflects an active, unresolved authentication failure. No secondary categories are needed because the SAML error and team-wide login failures describe the same issue.

### G48 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: HITL_QUEUE

The response correctly focuses on the 504 webhook timeouts, recommends the runbook's status-page check, and accurately states the retry intervals and the greater-than-15-minute delay condition. However, 'We are actively monitoring your request' is an unsupported claim of ongoing support activity. The status-page check gives the customer a concrete next step, though the reply does not explain what happens after that check. The tone is professional and concise but impersonal and does not acknowledge the disruption since Wednesday. The unsupported monitoring assurance prevents a passing score.
Triage: overall 5 (passed: True) - The primary category correctly identifies broken webhook deliveries, despite using spaces rather than underscores in the category label. Medium priority fits a single-integration failure with no stated production-wide outage or core-business blockage. Action is required because the customer reports ongoing 504 errors and requests assistance. No secondary support issues are warranted: the office move and new hires are background details, and the coffee-machine aside is unrelated to OmniFlow support.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The header checks, exponential backoff with jitter, and one-time 48-hour +50% quota increase are supported by the runbook. However, the reply invents operational status by stating that the account is being reviewed and the override is actively being processed. The runbook authorizes Tier-1 to grant relief but does not establish that anyone has initiated it. 'To resolve this immediately' also implies an unsupported resolution timeline. The response addresses the right issue and appropriately identifies temporary relief rather than an unsupported highest-tier escalation, but it should clearly distinguish available relief from confirmed action. Customer troubleshooting steps are concrete, while the support-side next step is misleading. The tone is professional and acknowledges the production impact, though mentioning the Admin Console adds unnecessary internal detail. The groundedness failure caps the overall score at 2.
Triage: overall 3 (passed: False) - The primary category correctly identifies quota exhaustion; its wording is an unambiguous equivalent of quota_rate_limit_exceeded. Action_needed is correctly true because production is actively blocked and escalation is requested. No secondary issue is warranted: the sync outage is a consequence of quota exhaustion, not a separate problem. However, the ticket explicitly describes production as completely down, supporting critical under the complete-production-outage guideline. High is understandable given the quota-blockage guideline, but understates the reported total outage. The draft reply is outside the scope of this evaluation.
