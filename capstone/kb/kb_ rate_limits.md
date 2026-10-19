# OmniFlow Runbook: API Quotas and 429 Throttling

**Category:** `quota_rate_limit_exceeded`  
**Applies to:** REST API v2, GraphQL API, Ingestion Endpoints

## Rate Limit Thresholds
- **Starter Plan:** 60 requests/minute | 10,000 requests/day
- **Pro Plan:** 300 requests/minute | 100,000 requests/day
- **Enterprise Plan:** 1,200 requests/minute | Custom daily ceilings

## Remediation Workflow
1. **Inspect Response Headers:**
   - Guide the customer to monitor `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` (Unix epoch seconds) in their client application.
2. **Implement Backoff:**
   - Instruct the client to implement exponential backoff with jitter when receiving HTTP status `429 Too Many Requests`.
3. **Temporary Emergency Burst:**
   - Tier-1 support may grant a one-time 48-hour temporary quota increase (+50%) via the Admin Console under **Tenants > [Tenant ID] > Overrides > Temporary Limit Relief** if production operations are blocked.

## Escalation Criteria
- If customer requests permanent quota increases, route the ticket to their Account Executive (AE) or Sales team with priority `LOW`.
