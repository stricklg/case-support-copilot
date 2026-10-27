# Capstone eval report

Run at: 2026-10-27T15:57:07.149219+00:00 (mode: live)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 86.0%

## Judge (draft replies)
- Cases judged: 33
- Avg groundedness: 2.45
- Avg accuracy: 2.79
- Avg actionability: 2.97
- Avg tone: 3.85
- Avg overall: 2.36
- Pass rate (overall = 5): 0.061
- Pass rate (overall >= 4): 0.242

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination HITL_QUEUE)

### G05 — not judged (status 200, destination HITL_QUEUE)

### G06 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply faithfully follows the runbook's HTTP 500/504 guidance: check the status page for ingestion pipeline delays and explain the exact retry intervals if delivery is delayed more than 15 minutes. It provides a clear customer action without inventing policies, timelines, or outcomes. However, the tone is flat and does not acknowledge the impact of failing contact-create webhooks. This prevents an excellent overall score, so the reply does not pass.

### G07 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The per-minute plan limits are correctly quoted, but the KB does not prescribe exponential backoff or describe an Enterprise upgrade process. These are invented next steps, a severe grounding failure under the rubric. The reply addresses the reported 429 errors and gives concrete suggestions, but those suggestions are not supported by the retrieved runbook. It also omits the documented daily limits, which could be relevant to a nightly batch sync. The tone is professional and concise but formulaic, with little acknowledgment of the disruption. Groundedness of 2 caps the overall score at 2; the reply fails.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats, the purchase path supported by the runbook, and applies the customer's requested quantity of 20 seats. It provides a clear customer action without inventing policies, timelines, or outcomes. The tone is concise, professional, and appropriate for a straightforward purchase request.

### G09 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

All technical instructions are directly supported by the runbook, with no invented settings or promises. The conditional JIT guidance correctly identifies the required assertions. However, the certificate-matching check is prescribed for signature errors, which the customer has not reported, and the reply does not clarify whether JIT is intended or what specific help is needed for the new subdomain. The checks are actionable, but there is no clear follow-up request or path after completing them. The tone is concise and professional, though somewhat impersonal.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: HITL_QUEUE

The KB does not establish whether parquet export is supported, define the product's export scope, or prescribe logging feature requests. The reply invents both a product limitation and a completed action ('We have logged your request'). Although it addresses the requested feature, its answer and next step cannot be verified against the runbook, which only provides escalation instructions for legal or regulatory requests. The claimed future evaluation is vague and unsupported. The tone is polite and concise, but these grounding failures cap the overall score at 2.

### G11 — not judged (status 400, destination None)

### G12 — not judged (status 400, destination None)

### G13 — not judged (status 400, destination None)

### G14 — not judged (status 400, destination None)

### G15 — overall 1 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The KB only provides an escalation path for accounts locked for non-payment when proof of a pending wire transfer is supplied; that scenario does not apply here. It does not authorize manual card retries, instruct customers to update billing settings, or state that finance will re-run a transaction. The reply invents all three and promises an unsupported next step. Although its instructions are concrete, they are not reliable or grounded. The tone is professional and concise, but offers little acknowledgment of the customer's inconvenience.

### G16 — overall 2 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: HITL_QUEUE

The refund authority up to $250 is supported by the runbook. However, the reply claims that account review and refund processing are happening now, although neither action is established by the provided context. It also implies the refund can proceed without determining whether the amount exceeds $250, which would require Finance escalation. The response addresses the duplicate charge and names a next step, but that step is unsupported and omits the applicable escalation condition. The tone is polite and concise, though mentioning internal approval limits is unnecessarily procedural. The groundedness failure caps the overall score at 2.

### G17 — overall 1 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The retrieved runbook provides no guidance on mid-cycle plan upgrades or proration; it only specifies escalation for accounts locked due to non-payment with proof of a pending wire transfer. The reply invents automatic daily proration and placement of the adjustment on the next scheduled invoice. These are central, unsupported billing claims. It also offers to proceed with the transition without any supporting procedure in the KB. Although the reply is concise, polite, and includes a clear customer question, its proposed next step is not grounded and it does not acknowledge the limits of the available information. It fails the rubric.

### G18 — not judged (status 200, destination HITL_QUEUE)

### G19 — overall 1 (passed: False)
Retrieved: kb_ billing_subscription.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The KB lists ACH as in scope but provides no procedure for changing payment methods. The reply invents a Billing section in workspace settings and an alternative finance-team workflow; neither is supported. The only documented finance escalation concerns locked accounts with proof of a pending wire transfer, which does not apply here. Although the reply addresses the requested change and offers concrete actions, those actions are unverified, and it does not establish how the requested next-month timing would be handled. The tone is polite, concise, and professional, but the unsupported instructions are a severe grounding failure.

### G20 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply correctly follows the invalid SAML response runbook: compare the IdP X.509 certificate with the certificate in Settings > Security > SSO and upload the new PEM before switching the IdP primary certificate during rollover. It provides a clear customer action and asks for follow-up if the issue persists, without inventing policies or timelines. However, the tone is flat and does not acknowledge that all users are unable to log in or the impact of that outage, so it falls short of the rubric's excellent standard.

### G21 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply accurately reproduces all three SCIM troubleshooting checks in the runbook: token expiration after 180 days, exact case-sensitive email matching, and available unassigned seats. It is fully grounded, addresses the reported provisioning issue, and clearly states what the customer should check. However, the tone is flat and does not acknowledge the impact of new employees being unable to access OmniFlow. This is a minor but real tone flaw under the rubric, so the overall score is 4 and the reply does not pass.

### G22 — overall 1 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The retrieved KB only identifies supported SSO categories and gives an escalation rule for admin lockouts. It provides no setup procedure. The reply invents dashboard navigation, creation of a SAML connection, and requirements for a distinct identifier and configuration URI. These are unsupported substantive steps, even if technically plausible. The response addresses the general topic but cannot establish the correct next steps from the supplied runbook. Its instructions are concrete but unreliable, and asking the customer to report errors does not remedy that gap. The tone is concise and professional, though impersonal. The unsupported setup instructions constitute a severe grounding failure, so the reply does not pass.

### G23 — overall 2 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply invents an operational step by stating that the team is reviewing the SSO configuration; the KB provides only escalation criteria and does not support that claim. It also treats the redirect loop as a confirmed authentication lockout without establishing whether admins are locked out. The conditional escalation broadly follows the runbook, but adds an unsupported requirement that all tenant admins be affected and omits the Enterprise qualifier. Asking the customer to report whether secondary local admin access exists is useful, but the reply should directly clarify whether Enterprise tenant admins are locked out with no active secondary local admin, then state that this condition requires immediate escalation. The tone is professional and concise, though it does not explicitly acknowledge the impact.

### G24 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The inspection path and Sanitize / Coerce Node recommendation are supported for payload schema mismatches. However, the reply makes an unsupported generalization that branch condition failures often stem from schema mismatches or strict typing. The customer reports a condition syntax error when comparing a field to a string, not a schema validation error, and the KB provides no fix for that specific syntax issue. The reply therefore applies a different issue's troubleshooting steps without establishing their relevance or acknowledging the KB's limitation. It gives concrete actions, but they may not address the reported failure. The tone is professional and concise, though it does not explicitly acknowledge the workflow disruption.

### G25 — overall 5 (passed: True)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The reply is fully grounded in the retrieved runbook: it identifies strict typing as the relevant cause, directs the customer to the exact Raw Input inspection path, and recommends a Sanitize / Coerce Node before branch evaluation. It provides concrete customer actions without inventing policies, timelines, or outcomes. The tone is professional and concise, though its acknowledgment of customer impact is somewhat formulaic. Overall, it meets the pass criteria.

### G26 — overall 2 (passed: False)
Retrieved: kb_ workflow_syntax.md | Category: workflow syntax/execution error | Destination: AUTOMATED_CRM

The 500ms threshold, backtracking protection, anchor optimization, and replacement of nested quantifiers are supported by the runbook. However, those instructions apply to ERR_REGEX_TIMEOUT, while the customer reports nonmatching ticket IDs, not a timeout. The reply assumes that the timeout guidance is relevant without establishing that condition and implies these changes will ensure successful execution. It offers concrete edits, but no step to establish whether the documented timeout issue applies. The tone is concise and polite but does not acknowledge the customer's difficulty. The response fails because it treats an unconfirmed timeout as the explanation for a different reported symptom.

### G27 — overall 2 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The reply claims that a team is investigating and promises updates shortly, neither of which is supported by the KB. It addresses the reported delays but omits the runbook's prescribed next step: immediate critical escalation if queue lag exceeds five minutes and affects multiple accounts. The ticket does not establish multi-account impact, so that condition needs verification rather than an unconditional escalation claim. The reply offers no concrete supported next step or clarification request. Its tone is professional and concise but generic, without acknowledging the impact of jobs finishing three hours late.

### G28 — overall 2 (passed: False)
Retrieved: kb_ performance_latency.md | Category: performance/latency issue | Destination: AUTOMATED_CRM

The reply correctly acknowledges delayed webhook delivery without failures and preserves the runbook’s conditional escalation threshold. However, it claims an active investigation and promises an update shortly after diagnosis, neither of which is supported by the KB. It also weakens the prescribed action into generic escalation language, omitting immediate escalation to incident response at CRITICAL priority if multiple accounts are affected. Because the ticket does not establish multi-account impact, immediate escalation cannot be assumed; the response should clarify that condition rather than imply an investigation is already underway. The next step remains vague. The tone is polite and concise but lacks explicit empathy for the impact and exposes internal runbook terminology. Unsupported operational claims cap the overall score at 2.

### G29 — not judged (status 200, destination HITL_QUEUE)

### G30 — overall 1 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: AUTOMATED_CRM

The reply invents a 24–48-hour sandbox provisioning timeline and a wait-until-tomorrow escalation procedure, neither of which appears in the KB. The only documented next step is HIGH-priority escalation to @partner-solutions for Enterprise White-Glove Onboarding tenants with launch blockers within 14 days of contract signature. The ticket does not establish those eligibility conditions, and the reply neither checks them nor explains the conditional escalation. Although it gives a concrete customer action, that action is unsupported and could delay appropriate handling. The tone is polite and concise but does not acknowledge the impact of the unavailable sandbox.

### G31 — overall 2 (passed: False)
Retrieved: kb_ onboarding_setup.md | Category: onboarding/environment setup | Destination: HITL_QUEUE

The reply invents a DNS investigation, an operations-team escalation, and a propagation check, none of which the runbook supports. The only documented escalation is to @partner-solutions at HIGH priority for Enterprise White-Glove tenants with launch blockers within 14 days of contract signature; the ticket does not establish those conditions. Although the reply addresses the CNAME issue and states a concrete next step, that step is unsupported and it does not seek the information needed to determine escalation eligibility. The tone is professional and concise but offers little acknowledgment of the customer's delay. The severe grounding failure caps the overall score at 2.

### G32 — not judged (status 200, destination HITL_QUEUE)

### G33 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The KB only prescribes immediate escalation to @legal-ops for formal legal preservation orders or regulatory-authority requests. This customer’s GDPR erasure request does not establish either condition. The reply invents routing to a legal and compliance operations team and a written-confirmation workflow, neither of which is supported for this request. It does not explicitly promise complete deletion, but it implies an unsupported process for addressing the requested scope. Although it states a next step, that step is not grounded in the runbook. The tone is professional and concise, but offers little acknowledgment of the customer’s concern. The groundedness failure caps the overall score at 2.

### G34 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The Trust Portal referral for the SOC 2 Type II report and the electronic NDA requirement for Standard-tier customers are supported by the runbook. However, the reply also claims that the data retention policy is available directly through the portal, which the KB does not establish. This invents an access path for one of the requested documents and is a significant grounding failure. The SOC 2 next steps are clear, but the retention-policy request remains unresolved despite being presented as answered. The tone is professional and concise, though somewhat impersonal. The groundedness score caps the overall score at 2.

### G35 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: data export compliance | Destination: HITL_QUEUE

The reply correctly identifies the requested Q3 audit log and admin actions, but invents an export workflow: the KB does not establish that a team is processing the request or that a secure download link will be provided. Its only prescribed action is immediate legal escalation for preservation orders or regulatory requests, neither of which is indicated here. The reply offers an apparently concrete next step, but that step is unsupported; the supplied KB does not establish how to fulfill this export. The tone is professional and concise, though somewhat formulaic. The severe grounding failure caps the overall score at 2.

### G36 — overall 2 (passed: False)
Retrieved: kb_ feature_request.md | Category: feature request | Destination: HITL_QUEUE

The reply correctly recognizes the Microsoft Teams integration request as product feedback, but invents a completed logging action, a feature tracking system, and review by the product development team. None is supported by the runbook, which only specifies routing for contractually negotiated custom features for qualifying Enterprise accounts; the ticket does not establish those conditions. The reply therefore presents an unsupported process rather than a grounded next step. Its tone is professional and concise, though it does not specifically acknowledge the customer's Teams-based workflow. The groundedness failure caps the overall score at 2.

### G37 — not judged (status 200, destination HITL_QUEUE)

### G38 — overall 4 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply accurately reproduces the runbook’s OAuth re-authentication and conditional HMAC key-regeneration steps, using the correct Salesforce navigation paths. It provides clear customer actions and introduces no unsupported policies or timelines. However, its tone is purely procedural: it does not acknowledge the disruption caused by rejected Salesforce events or express empathy. Under the rubric, that tone flaw prevents an overall score of 5, so the reply does not pass.

### G39 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply invents a troubleshooting step: updating a webhook secret in OmniFlow settings to match newly rotated Stripe API keys. The supplied runbook neither describes that setting nor establishes that relationship or remedy. It only provides conditional escalation criteria for sustained, multi-tenant validation failures and suspected data loss during month-end close. The reply addresses the reported symptom and gives a clear customer action, but that action is unsupported, and its generic investigation offer does not establish an applicable runbook-based next step. The tone is professional and concise, though it does not explicitly acknowledge the disruption. The severe grounding failure caps the overall score at 2.

### G40 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The reply invents an active support-engineering investigation into usage limits and rate-limit counters, neither of which is supported by the retrieved runbook. It also promises an update 'shortly' without any supported timeline. Although it acknowledges the reported GraphQL throttling, the KB provides only an escalation path for permanent quota-increase requests, which this customer has not made; it provides no investigation procedure for this issue. The reply therefore cannot substantiate its stated next steps. It offers no concrete customer action or reliable next step. The tone is professional, concise, and empathetic, but the severe grounding failures cap the overall score at 2.

### G41 — overall 2 (passed: False)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: AUTOMATED_CRM

The KB only specifies escalation for contested ownership disputes; it provides no standard transfer procedure or authorization requirements. The reply invents a requirement to verify administrative rights or supply written stakeholder confirmation and implies that this will enable the transfer. Although it addresses the requested ownership transfer and seat removal, its next step is unsupported. The customer ask is clear but not validly grounded, and no concrete seat-removal next step is given. The tone is professional and concise, but it does not acknowledge the customer's circumstances. Groundedness caps the overall score at 2; the reply does not pass.

### G42 — not judged (status 200, destination HITL_QUEUE)

### G43 — not judged (status 200, destination HITL_QUEUE)

### G44 — overall 1 (passed: False)
Retrieved: kb_ feature_request.md | Category: billing subscription issue | Destination: AUTOMATED_CRM

The retrieved runbook covers feature requests, not volume pricing or named account managers. Its only escalation rule applies to contractually negotiated custom features for Enterprise accounts with ARR above $50k, conditions not established by this ticket. The reply invents a completed routing action to a sales and account management team and an unsupported promise that they will respond shortly. It recognizes both customer questions but provides neither supported answers nor a valid runbook-prescribed next step. The claimed handoff sounds actionable but is ungrounded. The tone is professional and concise.

### G45 — not judged (status 200, destination HITL_QUEUE)

### G46 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The webhook response correctly identifies checking the status page as the next diagnostic step and quotes the documented retry intervals. However, it omits the condition that retry guidance applies when delivery is delayed more than 15 minutes. More seriously, the KB provides no billing procedure or evidence that the ticket was flagged for review, so claiming that action occurred and promising assistance 'shortly' are unsupported. The reply gives a concrete webhook next step but no grounded resolution path for the invoice question. Its tone is professional and concise, but it does not acknowledge the customer's disruption or billing concern empathetically. The groundedness failure caps the overall score at 2.

### G47 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: HITL_QUEUE

The reply is grounded in the runbook and appropriately directs the customer to compare the IdP X.509 certificate with the certificate in Settings > Security > SSO. It introduces no unsupported policies or timelines. However, its rollover guidance omits the required sequence: upload the new PEM certificate to OmniFlow before switching the primary certificate in the IdP. The certificate check is actionable, but the rollover instructions are incomplete. The tone is professional and acknowledges the team-wide issue, though responding in English rather than the customer's Spanish reduces accessibility. These flaws prevent a passing score.

### G48 — overall 2 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: AUTOMATED_CRM

The reply correctly identifies the 504 timeout issue and reproduces the runbook's status-page check and conditional retry intervals. However, it invents assurances that the team is actively monitoring the pipeline and will provide updates if further troubleshooting is required; neither is supported by the KB. This unsupported operational commitment caps the overall score at 2. The status-page check is concrete, but the reply shifts it to the customer rather than stating that support will perform the prescribed check, and its subsequent next step is unsupported. The tone is professional and concise but does not explicitly acknowledge the disruption.

### G49 — not judged (status 200, destination HITL_QUEUE)

### G50 — overall 2 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: AUTOMATED_CRM

The runbook permits routing to an Account Executive or Sales at LOW priority only when the customer requests a permanent quota increase. This customer requested urgent escalation for a production outage, not a permanent increase. The reply therefore applies a conditional escalation step without justification and invents permanent-increase handling as the purpose of the request. It states a concrete next step, but that step is unsupported for this ticket; the provided KB does not specify how to handle the requested urgent escalation. The tone is professional and acknowledges the outage, though it offers limited empathy. The groundedness failure caps the overall score at 2; the reply does not pass.
