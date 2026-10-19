# OmniFlow Runbook: Processing Delays and Latency Degradation

**Category:** `performance_latency_issue`  
**Applies to:** Async queues, batch processing delays, webhook delivery lag

## Diagnostic Steps
1. **Queue Lag vs. Execution Time:**
   - Check the **System Status Page** to verify whether platform-wide queue congestion is active.
   - Standard processing SLA: 95th percentile execution within 1.5 seconds. Delays > 30 seconds indicate queue backup.

2. **Tenant Throttling / Concurrency Saturation:**
   - Check if tenant is exhausting their max concurrent workflow threads (Standard: 10 threads; Enterprise: 50 threads).
   - When thread limits are saturated, incoming executions queue with state `QUEUED_BUFFERED`.
   - Recommend the customer space out upstream bulk cron dispatches.

3. **Downstream Receiver Backpressure:**
   - If OmniFlow webhooks show high dispatch latency, verify downstream server response latency (OmniFlow times out after 10s).

## Escalation Criteria
- Platform-wide queue lag exceeding 5 minutes affecting multiple accounts: Escalate immediately to `@incident-response` with priority `CRITICAL`.
