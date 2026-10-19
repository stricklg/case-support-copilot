# OmniFlow Runbook: Inbound Webhook Failures & Secret Rotation

**Category:** `integration_webhook_failure`  
**Applies to:** HubSpot, Salesforce, Stripe, and Custom Webhook Integrations

## Diagnostic Steps
1. **HTTP 401 Unauthorized / Expired Signatures:**
   - Verify if the client rotated their signing secret or OAuth token within the last 24 hours.
   - Instruct the customer to navigate to **Settings > Integrations > [Provider] > Connection Settings** and select **Re-authenticate via OAuth**.
   - If using HMAC secret verification, guide them to regenerate the signing key under **Developer Portal > Webhooks > Inbound Secrets**.

2. **HTTP 429 Too Many Requests:**
   - Webhook ingress throttles at 500 events/second per tenant on Standard tiers, and 2,500/sec on Enterprise.
   - Advise the customer to enable batch deliveries in their source platform or upgrade to Enterprise Ingress.

3. **HTTP 500 / 504 Timeouts:**
   - Check status page for ingestion pipeline delays.
   - If delivery is delayed > 15 minutes, inform the customer that automatic retry backoff occurs at 1m, 5m, 15m, 1h, and 6h intervals.

## Escalation Criteria
- If raw payloads fail validation for > 30 consecutive minutes across multiple tenants, flag as an **active incident** and escalate to `@oncall-integrations`.
- If data loss is suspected during month-end financial close, mark priority as `CRITICAL`.
