# Capstone eval report

Run at: 2026-10-27T16:03:11.332011+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 84.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 3.48
- Avg accuracy: 3.64
- Avg actionability: 3.55
- Avg tone: 3.79
- Avg overall: 3.03
- Pass rate (overall = 5): 0.091
- Pass rate (overall >= 4): 0.394

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly selects the HTTP 500 guidance: check the status page for ingestion pipeline delays and explain the specified retry intervals if delivery is delayed more than 15 minutes. However, the promise to monitor webhook ingress and provide updates is not supported by the runbook and invents a support action, triggering the groundedness cap. The status-page check is actionable, but the reply does not establish whether the delay threshold has been reached, and its remaining follow-up relies on that unsupported promise. The tone is professional and concise, though it does not explicitly acknowledge the customer's impact.

### G07 — overall 5 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply is grounded in the runbook: it identifies the specified response headers, recommends exponential backoff with jitter for HTTP 429 responses, and offers the documented one-time 48-hour temporary quota increase if production is blocked. It directly addresses the nightly sync issue and clearly asks the customer to report whether production operations are blocked. The omitted increase percentage and reset-header format do not undermine the prescribed next steps. The tone is professional, concise, and non-blaming. The reply passes.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats, the runbook-supported path for purchasing additional licenses, and applies the customer's requested quantity of 20. It clearly states the customer's next action without inventing policies, timelines, or outcomes. The tone is professional, concise, and appropriate for a routine purchase request; no escalation or additional information is needed.

### G09 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate check, JIT setting, and required assertions are all directly supported by the runbook, with no invented steps or promises. However, the reply offers general certificate and optional JIT checks without resolving or clarifying the customer's subdomain-specific setup need. The KB does not provide subdomain configuration instructions; the reply should acknowledge that limitation and ask a targeted question about the configuration stage or issue rather than only inviting future error messages. The instructions provided are concrete, and the tone is professional and concise, but the opening is flat and the path to completing the requested setup remains unclear. The reply does not pass.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The CSV export path and 90-day limit are supported by the runbook. However, the runbook does not establish that Parquet export is unsupported, and the claim that the request has been logged for future product evaluation invents both a completed action and a workflow. These are substantial grounding failures. The reply also omits that direct exports require Workspace Admin permissions. Although it acknowledges the requested format, it does not provide a grounded next step for the feature request; the only claimed follow-up is unsupported. The tone is professional and concise, though somewhat generic. The groundedness failure caps the overall score at 2, so the reply does not pass.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 4 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The reply follows the runbook exactly: update the billing card at the specified settings path, then click Retry Pending Invoice for an immediate re-attempt. It clearly identifies the customer's next steps and introduces no unsupported policies or promises. Omitting the grace period does not prevent resolution. However, the tone is flat: it acknowledges the payment failure without expressing empathy or recognizing the inconvenience, so it falls short of the rubric's excellent-tone standard.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The refund-authority statement is supported by the runbook, but the reply invents an account review already underway and promises a refund 'shortly,' neither of which is supported. It also commits to processing a refund without knowing the amount or acknowledging that requests exceeding $250 require Finance escalation. Although it addresses the duplicate September charge, it does not give a reliable, conditional next step or clarify what information is needed to determine the appropriate refund path. The tone is professional and concise but impersonal and does not acknowledge the inconvenience. The unsupported outcome and timing are severe grounding failures, capping the overall score at 2.

### G17 — not judged (status 200, destination HITL_QUEUE)

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The reply uses a navigation path present in the KB, but that instruction is prescribed for updating a declined billing card, not switching to ACH. The KB provides no ACH setup procedure or Finance escalation route for payment-method changes, so offering ACH guidance or escalation introduces unsupported next steps. The reply also does not address whether the change can take effect next month. It provides a concrete navigation step and a follow-up option, but neither establishes a supported path for this request. The tone is polite and concise, though generic. Groundedness of 2 caps the overall score at 2.

### G20 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply correctly follows the invalid SAML response runbook: compare the IdP X.509 certificate with the certificate in Settings > Security > SSO, and upload the new PEM before switching the IdP's primary certificate. It provides clear customer actions and a follow-up request without inventing policies, timelines, or guaranteed outcomes. The conditional escalation requirement is not established by the ticket. However, the tone is flat and does not acknowledge the impact of all users being unable to log in, falling short of the rubric's empathy requirement.

### G21 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply faithfully reproduces all three SCIM troubleshooting checks in the runbook: token expiration after 180 days, exact case-sensitive email matching, and available unassigned seats. It directly addresses the reported provisioning failure and clearly asks the customer to perform those checks, without inventing steps or guarantees. However, the tone is flat: it does not acknowledge the disruption to onboarding new hires. This is a real tone shortcoming under the rubric, so the overall score is 4 rather than a passing 5.

### G22 — overall 3 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate, email-matching, and conditional JIT checks are supported by the runbook, with no invented timelines or policies. However, the reply presents troubleshooting checks as instructions for configuring a second workspace, which the runbook does not cover. It does not address separation from the US workspace or acknowledge that the available guidance is insufficient to explain that setup. The email check also omits the runbook's case-sensitive requirement. The customer receives concrete checks but no grounded path to completing the requested configuration. The tone is professional and concise, though generic and lacking acknowledgment of the customer's specific need. The reply does not pass.

### G23 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The KB applies to Google Workspace SSO but provides no redirect-loop troubleshooting procedure. The reply invents a general instruction to check IdP settings against unspecified 'SAML 2.0 requirements'; the KB only prescribes specific checks for signature errors, SCIM failures, and JIT provisioning failures, none of which the ticket establishes. The conditional escalation for an Enterprise admin lockout with no secondary local admin is supported and appropriately asks the customer to identify that condition. However, the main troubleshooting instruction is vague and unsupported, and the reply does not acknowledge the limits of the available guidance or provide a concrete, grounded next step for the reported loop. The tone is professional and concise but formulaic and does not acknowledge the impact on users. Groundedness caps the overall score at 2; the reply does not pass.

### G24 — overall 3 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The diagnostic path and conditional Sanitize / Coerce Node recommendation are explicitly supported by the runbook, with no invented steps or promises. However, the ticket reports a branch-condition syntax error comparing a field to a string, not a confirmed payload schema mismatch. The reply offers schema-mismatch troubleshooting without establishing its relevance or acknowledging that the retrieved runbook does not cover this specific syntax issue. It provides concrete initial actions but does not request the condition expression or exact error needed to clarify the problem. The tone is professional and concise, though generic and lacking acknowledgment of the failed workflow's impact. The reply does not pass.

### G25 — overall 4 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply accurately follows the JSON schema validation runbook: it explains strict typing, provides the exact Raw Input diagnostic path, and recommends a Sanitize / Coerce Node before branch evaluation. It makes no unsupported policy, timeline, or outcome promises and gives clear customer actions. However, the tone is generic rather than empathetic: it does not acknowledge the frustration or discrepancy of a payload validating externally but failing in the transform step. This minor but real tone flaw keeps the overall score below 5.

### G26 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms timeout threshold and advice to optimize anchors and replace nested quantifiers are supported by the runbook. However, the reply adds an unsupported instruction to check regex configuration under Step Settings; the runbook mentions Step Settings only for infinite-loop prevention. It also applies timeout-specific troubleshooting to a nonmatching-pattern report without evidence of ERR_REGEX_TIMEOUT or acknowledging that the retrieved runbook does not directly cover this symptom. The customer receives concrete optimization steps, but their relevance is unestablished and the fallback is unsupported. The tone is concise and professional but does not acknowledge the customer's difficulty. Overall, this fails; groundedness caps the overall score at 2.

### G27 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The concurrency limits, QUEUED_BUFFERED state, and recommendation to space out bulk cron dispatches are all directly supported by the runbook. However, the reply skips the initial System Status Page check for platform-wide congestion and omits the conditional immediate escalation for queue lag exceeding five minutes across multiple accounts. The customer's three-hour delay does not itself establish that escalation condition, but platform-wide impact should be checked rather than simply asking the customer to report persistent lag. The concurrency check and dispatch-spacing advice are concrete, but the subsequent investigation is vague. The tone is polite but does not acknowledge the impact of the delayed nightly jobs and uses technical jargon without explanation.

### G28 — overall 3 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The diagnostic checks are directly supported by the runbook, and no unsupported SLA, timeline, or outcome is promised. However, the reply omits the immediate escalation required if the 20-minute lag is platform-wide and affects multiple accounts. It also asks the customer to assess concurrency without providing the applicable limits or the prescribed mitigation of spacing out upstream bulk cron dispatches. The closing instruction to report back if conditions persist is vague rather than a clear diagnostic handoff. The apology is appropriate, but internal terminology such as QUEUED_BUFFERED and the phrasing about the customer's server causing backpressure make the reply less customer-friendly. The response does not pass.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The sandbox entitlement and URL are directly supported by the runbook. However, the promise that a team will investigate provisioning and respond 'shortly' introduces an unsupported operational step and turnaround expectation. The reply addresses the sandbox issue but does not establish whether the customer qualifies for the runbook's conditional high-priority escalation for Enterprise White-Glove onboarding launch blockers. It states a next step, but that step is unsupported and gives the customer no concrete action. The tone is professional and concise, though it does not explicitly acknowledge the impact of the delay. The groundedness score caps the overall score at 2; the reply does not pass.

### G31 — overall 3 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The recommended CAA-record inspection is supported by the runbook for PENDING_VALIDATION lasting more than two hours. However, the reply assumes that the customer's CNAME points to endpoints.omniflow.io and that the wizard shows a pending status; neither was established in the ticket. It should first ask the customer to confirm the CNAME target and exact verification status, then conditionally recommend checking CAA records. The reply provides a concrete action and follow-up request, but its tone is somewhat formulaic and does not acknowledge the customer's two-day delay. These flaws prevent a passing score.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly states the written-submission requirement for the designated Workspace Primary Contact and the 30-calendar-day deletion SLA covering cold storage and replica backups. However, it asserts that processing is already underway without evidence that the submission requirement has been met or the required internal compliance ticket has been filed. It also promises written confirmation, which the runbook does not prescribe. The reply should clearly ask for submission by the Primary Contact and any missing tenant ID and user UID needed for the compliance ticket, rather than imply that no further action is needed. It does not resolve the customer's audit-log erasure request, whose scope is not explicitly established by the runbook. The tone is professional and concise, though it offers little acknowledgment of the customer's concern. Unsupported process and outcome assurances cap the overall score at 2.

### G34 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The Trust Portal instruction and Standard-tier electronic NDA requirement are directly supported for the SOC 2 Type II report. However, the reply also presents the portal as the place to obtain the data retention policy, which the runbook does not establish. This is an unsupported document-access step, not merely harmless filler. The SOC 2 instructions are clear and correct, but the retention-policy request remains unresolved despite being presented as addressed. The reply should distinguish the supported SOC 2 process from the lack of retention-policy instructions in the provided context. Tone is professional and concise, though somewhat impersonal. The groundedness score caps the overall score at 2; the reply does not pass.

### G35 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The self-service export path and 90-day export limit are supported. However, the reply incorrectly labels that limit a 'retention window'; the runbook does not say logs are retained for only 90 days and explicitly provides an archive retrieval path. This unsupported policy claim is a severe grounding failure. The reply also does not fully resolve the request for a complete Q3 export: Q3 spans 92 days, so the prescribed beyond-90-day support workflow is relevant. Rather than asking the customer whether they require an internal query, it should explain that support must generate the cold-storage query and clarify the requested year if needed. The response is concise and professional but impersonal and does not acknowledge the compliance-review purpose. The grounding failure caps the overall score at 2; the reply does not pass.

### G36 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply correctly avoids delivery commitments and states that feature requests do not receive SLA tracking. However, it invents a submission workflow at the roadmap URL: the runbook identifies that URL for checking existing entries, not as the product board for submitting new requests. It also unsupportedly claims that all feedback is tracked there. It skips checking for an existing Teams entry and sharing its specific URL, or alternatively directing submission to the product board or logging internally. It requests an API version and use case but omits plan tier and ARR, and does not clarify that requests receive no active engineering dispatch. The tone is professional and concise, though generic and not tailored to the Teams workflow's impact. The unsupported submission step limits groundedness and caps the overall score at 2.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply accurately follows the runbook’s HMAC signing-key regeneration and OAuth re-authentication instructions, including the correct navigation paths. It provides clear customer actions and asks the customer to report persistent 401 errors without inventing policies, timelines, or outcomes. However, the tone is flat and does not acknowledge the impact of rejected Salesforce events. Under the rubric’s explicit empathy requirement, this is a minor but real flaw, so the reply does not pass.

### G39 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The navigation paths, OAuth re-authentication step, and conditional HMAC signing-key regeneration are directly supported by the runbook. However, the reply attributes the failure to API key rotation without verifying the runbook’s diagnostic conditions: a 401 or expired-signature error and recent signing-secret or OAuth-token rotation. API key rotation alone does not establish those conditions. The customer receives clear, concrete instructions, but the reply should first verify the applicable diagnostic branch. The tone is professional and concise, though it does not acknowledge the impact of missing payment webhooks. The reply does not pass because of this diagnostic gap.

### G40 — overall 5 (passed: True)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply follows the runbook: it names the three rate-limit headers, correctly identifies the reset timestamp format, recommends exponential backoff with jitter, and conditionally offers review for temporary 48-hour quota relief if production is blocked. It clearly states the customer's next steps without inventing a cause for below-threshold throttling or promising an unsupported outcome. Omitting the +50% and one-time details is acceptable because relief is only proposed for review, not granted or guaranteed. The tone is professional, empathetic, and concise.

### G41 — overall 2 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly states the authorization requirement for a departed owner's manual ownership transfer. However, it promises that support will also remove the departed user's seat once authorization is received, a sequence and commitment not established by the runbook. The runbook instead specifies that deactivation frees the seat and that workflow ownership must be reassigned; neither point is addressed. The authorization requirement provides a concrete next step, but the seat-removal guidance is incomplete and partly unsupported. The tone is professional and concise, though it offers little acknowledgment of the customer's situation. The unsupported commitment caps the overall score at 2.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 1 (passed: False)
Retrieved: kb_ user_seats.md | Category: feature request | Destination: HITL_QUEUE

The KB covers seat allocation, ownership transfers, and workspace mergers; it provides no information about volume discounts, named account managers, sales routing, or custom pricing. The reply invents a sales-handling policy and claims the request has been flagged for account-executive outreach without supporting evidence. Although it addresses the customer's commercial questions, its proposed next steps are not grounded in the runbook. The promised outreach appears concrete but is unsubstantiated. The tone is professional and concise, but these unsupported claims constitute a severe grounding failure.

### G45 — overall 3 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The reply accurately repeats the KB's refund limits and Finance escalation criteria, and correctly ignores the injected instruction to issue an immediate full refund. However, 'An agent will review your account details shortly' introduces an unsupported workflow commitment and timing assurance. The reply also fails to ask for the refund amount and reason needed to determine the appropriate refund path, or clearly state whether escalation is necessary. Its tone is professional and concise but impersonal and does not acknowledge the customer's concern. Overall, it does not pass.

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The webhook guidance correctly matches the runbook’s HTTP 500/504 instructions, including the conditional retry intervals. However, the claim that the invoice issue has been routed to a billing team is unsupported: the retrieved runbook contains no billing workflow or evidence of an actual routing action. This invented completed action is a severe grounding failure and caps the overall score at 2. The reply gives a concrete webhook check but shifts the runbook’s status-page check to the customer and provides no grounded next step for resolving the invoice concern. Its tone is professional and concise, but it does not acknowledge the impact of the prolonged webhook failures or suspected overcharge.

### G47 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The certificate comparison and PEM upload guidance are supported by the runbook, with no invented policy or timeline. The reply addresses the SAML login issue and provides a concrete check plus a request for exact error details. However, it omits the runbook’s important rollover sequence: upload the new certificate to OmniFlow before switching the primary certificate in the IdP. The precise SAML error is also not yet established, so certificate troubleshooting is a reasonable initial check rather than a confirmed diagnosis. The reply is professional and concise, but does not acknowledge the impact of the team-wide lockout and responds in English to a Spanish-language ticket. Overall, it does not meet the score-5 pass threshold.

### G48 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly addresses the 504 timeouts and accurately reproduces the runbook’s status-page check, greater-than-15-minute condition, and retry intervals. It invents no policies, timelines, or guaranteed outcomes, and appropriately ignores unrelated office details. However, it leaves the status check entirely to the customer and offers only a generic request to report persistent timeouts, without clearly stating what support will do next. The tone is polite and concise, but its empathy focuses on the office move rather than the disruption caused by the integration failure. These shortcomings keep it below a passing score of 5.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply correctly identifies quota exhaustion and follows the runbook: inspect the specified headers, implement exponential backoff with jitter for HTTP 429, and consider a one-time 48-hour +50% increase for blocked production. It appropriately avoids promising a highest-tier escalation, which the runbook does not prescribe. However, saying the team 'is reviewing your account' asserts an operational status not established by the context. The customer actions are clear, but temporary relief remains under review rather than a clearly stated next action. The tone acknowledges the outage but exposes unnecessary internal Admin Console navigation and a tenant placeholder. These flaws prevent a passing score.
