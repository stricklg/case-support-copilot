# OmniFlow Runbook: Sandbox vs Production & Onboarding Setup

**Category:** `onboarding_environment_setup`  
**Applies to:** Sandbox provisioning, custom CNAME domains, initial setup

## Operational Procedures
1. **Sandbox vs. Production Environments:**
   - Every Pro and Enterprise account includes one isolated sandbox environment (`sandbox.omniflow.internal/[tenant]`).
   - Sandboxes share plan limits but cannot execute external webhook pushes unless **Outbound Live Mode** is explicitly enabled in Sandbox Settings.

2. **Custom Domain / CNAME Routing:**
   - Setup requires customer to create a DNS `CNAME` pointing to `endpoints.omniflow.io`.
   - SSL certificates are automatically provisioned via Let's Encrypt within 60 minutes of DNS propagation.
   - If status shows `PENDING_VALIDATION` > 2 hours, instruct user to inspect CAA DNS records for conflicts.

3. **Initial Workspace Migration:**
   - Direct users to the **Quickstart Guide** and pre-built workflow templates gallery.

## Escalation Criteria
- Enterprise White-Glove Onboarding tenants experiencing launch blockers within 14 days of contract signature: Escalate to `@partner-solutions` with priority `HIGH`.
