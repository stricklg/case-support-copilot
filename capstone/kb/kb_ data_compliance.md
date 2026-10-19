# OmniFlow Runbook: Data Export, Audit Logs, and Compliance

**Category:** `data_export_compliance`  
**Applies to:** GDPR/CCPA erasure, SOC 2 reports, audit log dumps, data retention

## Standard Operating Procedures
1. **Audit Log Export:**
   - Workspace Admins can export up to 90 days of security and activity logs directly via **Settings > Security > Audit Log > Export CSV**.
   - For log requests beyond 90 days (Enterprise archive), support must generate a cold-storage query via internal portal.

2. **Right to Be Forgotten / GDPR Data Deletion:**
   - All erasure requests must be submitted in writing by the designated Workspace Primary Contact.
   - Support agents must file an internal ticket via `/ops-compliance dpo-request` with the tenant ID and user UID.
   - Deletion SLA is 30 calendar days across cold storage and replica backups.

3. **SOC 2 Type II & Penetration Test Reports:**
   - Direct customer to the **Trust Portal** (`trust.omniflow.internal`).
   - Customers on Standard tiers must sign an electronic NDA on the portal before automated report download.

## Escalation Criteria
- Formal legal preservation orders or requests from regulatory authorities: Mark priority as `CRITICAL` and forward immediately to `@legal-ops`.
