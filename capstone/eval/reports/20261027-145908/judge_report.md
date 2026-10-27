# Capstone eval report

Run at: 2026-10-27T14:59:41.657430+00:00 (mode: replay)
Generator: gemini-3.5-flash-lite (fallback gemini-3.8-flash) | Judge: gpt-6.1-sol

## Benchmark
- Schema compliance: 100.0%
- Routing accuracy: 90.0%

## Judge (draft replies)
- Cases judged: 5
- Avg groundedness: 4.0
- Avg accuracy: 4.0
- Avg actionability: 3.8
- Avg tone: 4.0
- Avg overall: 3.6
- Pass rate (overall = 5): 0.2
- Pass rate (overall >= 4): 0.6

## Per-case judge notes

### G01 — not judged (status 400, destination None)

### G02 — not judged (status 400, destination None)

### G03 — not judged (status 400, destination None)

### G04 — not judged (status 200, destination RoutingDesignation.HITL_QUEUE)

### G05 — not judged (status 200, destination RoutingDesignation.HITL_QUEUE)

### G06 — overall 3 (passed: False)
Retrieved: kb_webhook_failure.md | Category: integration webhook failure | Destination: RoutingDesignation.AUTOMATED_CRM

The reply correctly selects the HTTP 500/504 guidance, directs the customer to check the status page, and accurately states the conditional retry schedule. However, the promise to investigate further and provide updates is not supported by the runbook. It also leaves the next step unclear if the status page shows no delays. The escalation criteria are not established by the ticket, so escalation is not yet required. The tone is polite but does not acknowledge the customer's disruption, and 'L1 Support' and 'ingestion pipeline' introduce unnecessary internal jargon.

### G07 — overall 4 (passed: False)
Retrieved: kb_ rate_limits.md | Category: quota/rate limit exceeded | Destination: RoutingDesignation.AUTOMATED_CRM

The response is fully grounded in the runbook: it identifies the appropriate headers, recommends exponential backoff with jitter, and conditionally offers evaluation of the documented 48-hour, +50% temporary increase. It clearly states the customer's next steps and asks them to report whether production is blocked, without promising relief. However, the tone does not acknowledge the disruption to the nightly sync, and the reference to the Admin Console exposes unnecessary internal tooling jargon. These are minor but real tone flaws under the strict pass criteria.

### G08 — overall 5 (passed: True)
Retrieved: kb_ user_seats.md | Category: user/seat management | Destination: RoutingDesignation.AUTOMATED_CRM

The reply correctly directs the customer to Billing > Manage Seats, the purchase path explicitly supported by the runbook, and incorporates the requested quantity of 20 seats without inventing policies, timelines, or outcomes. The customer’s next action is clear. The tone is concise, professional, and appropriate for a straightforward purchase request; no impact acknowledgment is necessary because the customer reported no disruption.

### G09 — overall 4 (passed: False)
Retrieved: kb_ sso_provisioning.md | Category: auth/sso provisioning | Destination: RoutingDesignation.AUTOMATED_CRM

The certificate check, JIT toggle, and required firstName, lastName, and email assertions are all supported by the runbook, with no invented configuration details or promises. However, the certificate check is prescribed for signature-mismatch errors, which the customer has not reported, and the reply does not clarify whether JIT provisioning is intended or what specific help is needed for the new subdomain. The checks are actionable, but asking only for error codes leaves the setup request incompletely addressed. The tone is professional and concise but somewhat impersonal.

### G10 — overall 2 (passed: False)
Retrieved: kb_ data_compliance.md | Category: feature request | Destination: RoutingDesignation.HITL_QUEUE

The KB documents CSV audit-log exports, but does not establish that Parquet is unsupported or authorize logging feature requests with the product team. The claim that the request has already been logged invents a completed action, a severe grounding failure. The reply recognizes the requested format but substitutes an unsupported feature-request workflow for grounded guidance. Its stated next step is therefore unreliable. The tone is professional and concise, though it offers little acknowledgment of the customer's need. Overall is capped at 2 by groundedness.
