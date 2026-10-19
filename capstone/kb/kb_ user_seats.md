# OmniFlow Runbook: Workspace Management, Seats & Ownership Transfers

**Category:** `user_seat_management`  
**Applies to:** Seat allocation, workspace mergers, primary ownership transfer

## Common Tasks & Resolutions
1. **Workspace Ownership Transfer:**
   - Existing Primary Owner can transfer control directly via **Settings > Team > Roles > Transfer Ownership**.
   - **Departed Owner Protocol:** If current owner has left the organization without transferring, require written authorization from a verified company domain email matching HR/Executive leadership or legal before manual transfer.

2. **Seat Limit Reached:**
   - When inviting users fails with "Seat Limit Reached", instruct admin to purchase additional licenses via **Billing > Manage Seats** or revoke access for inactive seats.
   - Deactivating a member instantly frees their seat license; workflow ownership must be reassigned.

3. **Workspace Mergers:**
   - Workspaces cannot be merged automatically via the UI.
   - Guide client to export workflows as JSON definitions from Workspace A and import them into Workspace B.

## Escalation Criteria
- Contested ownership disputes between company stakeholders: Escalate immediately to `@security-compliance` with priority `MEDIUM`.
