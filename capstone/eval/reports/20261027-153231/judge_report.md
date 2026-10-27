# Capstone eval report

Run at: 2026-10-27T15:37:20.768168+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 82.0%

## Judge (draft replies)
- Cases judged: 29
- Avg groundedness: 3.48
- Avg accuracy: 3.45
- Avg actionability: 3.62
- Avg tone: 3.79
- Avg overall: 3.0
- Pass rate (overall = 5): 0.034
- Pass rate (overall >= 4): 0.414

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The status-page check and retry intervals, including the greater-than-15-minute condition, are directly supported by the runbook. However, the reply invents ongoing ticket monitoring and promises escalation if validation failures continue, omitting the required conditions of more than 30 consecutive minutes across multiple tenants. This materially broadens the escalation policy. The reply addresses the correct HTTP 500 category and gives a concrete status-page check, but does not explain what the customer should do after that check. Its tone is polite and concise, though it does not acknowledge the customer's impact and uses internal terminology such as 'L1 Support' and 'raw payloads.' The unsupported monitoring and escalation commitments cap the overall score at 2.

### G07 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply is fully grounded in the runbook: it identifies the relevant headers, recommends exponential backoff with jitter, and conditionally offers evaluation for a one-time 48-hour quota increase if production is blocked. It gives clear customer actions without promising relief. Omitting the +50% amount and reset timestamp format does not make the guidance incorrect. However, the tone merely restates the error rather than acknowledging the disruption to the customer's nightly sync, making it somewhat flat against the rubric's explicit empathy requirement.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats, the runbook-supported route for purchasing additional licenses. It addresses the requested 20-seat expansion without inventing pricing, approval requirements, or timelines. The next action is clear, and the tone is professional, concise, and appropriate for a routine purchase request. The reply passes.

### G09 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate check, JIT setting, and required firstName, lastName, and email assertions are all directly supported by the runbook. No policies, timelines, or configuration values are invented. However, the certificate check is prescribed for signature-mismatch errors, which the customer has not reported, and the reply does not distinguish these troubleshooting checks from instructions for configuring a new subdomain. The JIT guidance is appropriately conditional and actionable, but asking whether JIT is intended and what configuration assistance is needed would better establish the next step than asking only for errors. The tone is professional and concise, though generic. Overall, the response is grounded but does not fully resolve or clarify the setup request.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The CSV export path and 90-day limit are supported by the runbook. However, the runbook does not establish that Parquet is unsupported, and the claim that a feature request has been recorded for the product team invents both a workflow and a completed action. The reply addresses the requested format but gives an unsupported definitive answer. It also leaves the Enterprise archive process vague rather than explaining that support generates a cold-storage query for requests beyond 90 days. The tone is polite and concise, but these substantial grounding failures cap the overall score at 2.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 4 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply accurately follows the card-decline runbook: update the card using the specified settings path, then click Retry Pending Invoice for an immediate retry. It clearly states the customer's next steps and invents no policies, timelines, or support actions. Omitting the grace period does not prevent resolution. However, the tone is flat: it acknowledges the failed payment but not its impact or the customer's inconvenience. Under the rubric's strict pass criteria, this tone shortcoming keeps the overall score below 5.

### G16 — not judged (status 200, destination HITL_QUEUE)

### G17 — overall 1 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The KB does not explain mid-cycle plan upgrades or proration. The reply invents both automatic prorated charges and their application to the next scheduled invoice, presenting an unsupported billing outcome as fact. The subscription-review instruction is also not supported: the KB provides a billing path for updating payment methods, not reviewing subscription details. The reply should acknowledge that the available guidance does not establish how upgrade proration works rather than assert a policy. It offers no concrete next step to obtain a verified answer. The tone is polite and concise but generic.

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — not judged (status 200, destination HITL_QUEUE)

### G20 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately follows the runbook’s certificate-mismatch checks and certificate-rollover ordering, without inventing policies, timelines, or outcomes. It gives a concrete customer action and asks for follow-up if the issue persists. The conditional escalation rule is not clearly triggered by the information provided. However, the tone is generic and does not acknowledge the impact of login failing for all users, so it falls short of the rubric’s excellent standard.

### G21 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately presents all three SCIM troubleshooting checks prescribed by the runbook: token expiration after 180 days, case-sensitive email matching, and available unassigned seats. It clearly asks the customer to perform these checks and introduces no unsupported steps or timelines. However, the tone is generic and does not acknowledge the impact of new employees being unable to access OmniFlow. This minor but real tone shortcoming keeps it below the rubric's excellent-only passing threshold.

### G22 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply repurposes troubleshooting guidance as a new-workspace setup procedure that the KB does not provide. The KB supports checking certificate matching for signature errors, but does not establish that uploading a certificate is the prescribed next step for configuring a separate European workspace. It also treats JIT as required for SSO and implies that enabling JIT sends assertions; the KB only says to check JIT when automatic account creation fails and that the IdP must send those assertions. The reply gives concrete actions, but does not resolve the separate-workspace requirement or acknowledge the runbook's lack of setup instructions. Its tone is professional and concise, though minimally empathetic. These unsupported setup instructions cap the overall score at 2.

### G23 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The runbook does not provide a resolution for Google Workspace redirect loops. The reply invents a redirect-loop troubleshooting step by recommending matching unspecified SAML configuration attributes and the X.509 certificate; the certificate check is supported only for the distinct signature-mismatch scenario. It should acknowledge the lack of applicable guidance rather than present that check as a documented fix. The conditional immediate escalation for admin lockout without a secondary local admin is substantially grounded, although it omits the Enterprise qualifier. The reply provides a concrete check and a clear request to report admin lockout, but neither establishes a supported next step for the reported redirect loop. Tone is professional and concise, though it does not explicitly acknowledge the disruption. Groundedness caps the overall score at 2.

### G24 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The navigation path and Sanitize / Coerce Node recommendation are directly supported by the runbook, but only for JSON schema/type mismatch failures. The ticket reports a branch condition syntax error when comparing a field to a string; nothing establishes a schema mismatch. The reply therefore introduces an unsupported diagnosis and applies guidance for a different failure category. The runbook does not provide a fix for this specific syntax issue, so the reply should acknowledge that limitation rather than imply that coercion will resolve it. The steps are concrete but not established as appropriate; requesting the exact condition and error message would help clarify the issue. Tone is polite and concise, though it does not explicitly acknowledge the workflow disruption.

### G25 — overall 4 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply is fully grounded in the runbook: it explains strict typing, provides the exact validation path, and recommends a Sanitize / Coerce Node before branch evaluation. The customer has clear next steps, and no unsupported policies, timelines, or outcomes are introduced. However, the tone is flat: it restates the error without acknowledging the frustration or apparent inconsistency of a payload validating externally but failing in the transform step. Under the rubric's explicit empathy requirement, this keeps the overall score below 5.

### G26 — not judged (status 200, destination HITL_QUEUE)

### G27 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The thread limits, QUEUED_BUFFERED state, System Status Page check, and recommendation to space out bulk cron dispatches are directly supported by the runbook. However, the claims that support is reviewing and actively investigating the issue are unsupported assurances. The response addresses the correct issue but omits the runbook's conditional immediate escalation when platform-wide queue lag exceeds five minutes and affects multiple accounts; the reported batch delay alone does not establish that condition. Customer diagnostic actions are clear, but the reply does not explain what follows if platform congestion is confirmed. The tone is professional but impersonal, does not acknowledge the impact of the three-hour delay, and uses unexplained technical jargon. Overall, it does not pass.

### G28 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The reply is grounded in the runbook: status-page checks, concurrency saturation, QUEUED_BUFFERED, and the 10-second timeout are all supported. It addresses delivery lag with the correct diagnostic categories. However, it omits the actual concurrency limits needed to perform the tenant check and the recommendation to space out upstream bulk cron dispatches. It also does not explain that confirmed platform-wide lag exceeding five minutes across multiple accounts requires immediate escalation; the reported twenty-minute delay makes that conditional next step particularly relevant. The customer has concrete checks to perform, but the subsequent handling is reduced to vague further assistance. The tone is polite and empathetic, though internal terminology such as 'tenant' and 'QUEUED_BUFFERED' makes it less customer-friendly.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The sandbox entitlement and URL are supported by the runbook, but the claims that support is actively investigating provisioning and will follow up shortly once provisioning is complete are unsupported. They invent an operational step, imply a timeline, and promise an outcome the KB does not establish. The reply addresses the reported issue but does not establish the customer's plan or whether the conditional Enterprise White-Glove launch-blocker escalation applies. Its stated next step is therefore not grounded, and it asks for no information to clarify eligibility. The tone is polite and concise, but 'L1 Support' is internal jargon and the reply does not acknowledge the customer's delay or impact. Groundedness caps the overall score at 2; the reply does not pass.

### G31 — not judged (status 200, destination HITL_QUEUE)

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 4 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately states the written-request requirement, designated Workspace Primary Contact requirement, and 30-calendar-day SLA covering cold storage and replica backups, all directly supported by the runbook. It gives a clear customer action and a grounded next step. However, it does not address the customer's specific request concerning audit logs or written confirmation, nor clarify that the runbook does not establish those details. It also omits the tenant ID and user UID needed for the internal compliance request, although it appropriately avoids exposing internal commands. The tone is professional and concise but offers little acknowledgment of the request's significance. These omissions prevent an overall score of 5.

### G34 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly directs the customer to the Trust Portal for the SOC 2 Type II report and accurately states the Standard-tier electronic NDA requirement. However, it invents availability of data retention documentation through the portal; the runbook provides no location or retrieval procedure for that policy. This unsupported access instruction is a substantive grounding failure and caps the overall score at 2. The SOC 2 next step is clear, but the retention-policy request is not reliably addressed. The tone is professional and concise, though it does not acknowledge the customer's audit needs.

### G35 — overall 3 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply accurately reproduces the runbook’s 90-day self-service export limit and support-managed cold-storage query process without inventing policies or timelines. However, it does not apply those instructions to the requested full Q3 export: Q3 spans 92 days, so a complete quarter exceeds the self-service limit. It should clearly identify the support-managed export as the next step and clarify which year is requested. It also leaves the requested coverage of all admin actions unaddressed, although the KB does not establish that coverage and the reply should not promise it. The tone is professional and concise but lacks acknowledgment of the compliance need and includes unnecessary internal jargon such as 'cold-storage queries' and 'internal portal.'

### G36 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply claims the request has been logged on the public roadmap without evidence that a roadmap search or logging occurred. The runbook requires checking for an existing entry and sharing its specific URL, or directing submission/logging a new request via the prescribed process. The general board link does not establish an entry the customer can upvote or follow. The reply also omits collecting required request details and clarifying that feature requests receive neither SLA tracking nor active engineering dispatch. It correctly avoids delivery commitments and is professional and concise, though it does little to acknowledge the customer's workflow impact. The unsupported completed-action claim caps the overall score at 2.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly identifies the relevant 401/signature-verification issue and provides the runbook's exact location for regenerating an HMAC signing key. However, the runbook does not explicitly establish that these failures are 'expected' after rotation or instruct the customer to update the key to match Salesforce; these are unsupported additions to an otherwise grounded instruction. The reply also omits checking whether rotation occurred within the last 24 hours and the prescribed OAuth re-authentication instruction. The regeneration step and request to report continued issues are actionable. The tone is professional and concise, though it does not acknowledge the impact of rejected events. These flaws prevent a passing score.

### G39 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply uses only remediation steps explicitly supported by the runbook, correctly names Stripe, and clearly tells the customer what to do and when to follow up. However, it skips the runbook's diagnostic verification of whether a signing secret or OAuth token was rotated within the last 24 hours, treating the reported API-key rotation as sufficient to select the authentication-failure path without confirming that condition. The tone is professional and concise but does not acknowledge the impact of missing payment webhooks. These are real omissions, so the reply does not meet the all-excellent passing standard.

### G40 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply correctly follows the runbook by recommending the specified response headers, exponential backoff with jitter, and conditional 48-hour relief of +50% when production is blocked. However, it omits that temporary relief is one-time, an important policy limitation, and adds an investigation commitment that the runbook does not prescribe. The next steps are concrete, but mentioning the Admin Console exposes unnecessary internal tooling. These flaws prevent a passing score.

### G41 — overall 3 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly applies the departed-owner protocol and clearly requests written authorization from an appropriate verified company-domain email. However, it promises seat removal without mentioning the runbook's requirement to reassign workflow ownership when deactivating a member. The seat-removal portion is therefore incomplete, although deactivation freeing a seat is supported by the KB. The tone is professional and concise but does not acknowledge the customer's situation or impact. The missing workflow-reassignment step prevents a passing score.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The retrieved runbook covers feature requests, not volume pricing or named account management. It does not authorize a sales referral for this inquiry or support the promise that an Account Executive will follow up shortly. Its Account Executive escalation applies only to contractually negotiated custom features for Enterprise accounts with ARR above $50k, none of which is established here. The reply recognizes the customer's commercial inquiry but neither answers it with supported information nor provides a grounded next step. The promised follow-up sounds concrete but is unsubstantiated. The tone is professional and concise. The severe grounding failure caps the overall score at 2.

### G45 — not judged (status 200, destination HITL_QUEUE)

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The retry intervals and status-page check are supported by the runbook, but retry guidance is conditional on delivery delays exceeding 15 minutes, which the reply does not establish. More importantly, the claim that support has flagged the invoice for review and will assist shortly invents an action and service expectation absent from the retrieved KB. The webhook guidance is partly correct, but it shifts the status-page check to the customer and provides no clear follow-up based on the result. The invoice issue has no grounded next step. The tone is professional and concise but lacks acknowledgment of the customer's disruption. The unsupported billing claims cap the overall score at 2.

### G47 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

La respuesta se fundamenta en el runbook: indica comprobar el certificado X.509, respeta el orden de renovación del certificado PEM y contempla la escalación por bloqueo de administradores sin acceso local secundario. Sin embargo, condiciona esa escalación a que el problema persista tras las comprobaciones, cuando el runbook exige escalar inmediatamente si se cumple el criterio de bloqueo. Tampoco solicita confirmar si hay administradores afectados sin acceso local secundario, información necesaria para determinar la urgencia. El tono es profesional y conciso, pero no reconoce el impacto del bloqueo de todo el equipo desde ayer.

### G48 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly identifies the 504 timeout issue and names the prescribed status-page check. The retry intervals match the runbook, but the reply presents them unconditionally rather than tying them to delivery delays exceeding 15 minutes; that threshold has not been established. It also promises a follow-up 'shortly' with further troubleshooting steps, although the runbook supplies neither that timeline nor those additional steps. The status-page check is a concrete next action, but the subsequent plan is vague. The tone is professional and concise, though it acknowledges the office move more than the impact of the integration failure. The unsupported timing and broadened retry claim prevent a pass and cap the overall score at 2.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply accurately cites the prescribed headers, exponential backoff with jitter, and the permitted +50% temporary increase for 48 hours. It appropriately pursues temporary relief rather than inventing a highest-tier escalation. However, it omits that relief is one-time and says only that the account is being reviewed, leaving the actual granting of relief unclear. The tone acknowledges the outage but is mechanical and exposes internal Admin Console navigation that is not useful to the customer. These shortcomings keep it below a pass.
