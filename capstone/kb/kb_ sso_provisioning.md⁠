# OmniFlow Runbook: SAML 2.0 & Okta / Entra SSO Provisioning

**Category:** `auth_sso_provisioning`  
**Applies to:** Enterprise SAML, Okta, Microsoft Entra ID, Google Workspace SSO

## Common Scenarios & Resolution
1. **Error: "Invalid SAML Response / Signature Mismatch"**
   - Confirm that the customer's Identity Provider (IdP) X.509 certificate matches the certificate uploaded in **Settings > Security > SSO**.
   - Certificate rollovers require uploading the new PEM certificate to OmniFlow *before* switching the primary cert in the IdP.

2. **Error: "User Not Provisioned (SCIM Failure)"**
   - Check if the SCIM bearer token has expired (tokens are valid for 180 days).
   - Ensure the user's `email` attribute matches their OmniFlow account address exactly (case-sensitive).
   - Verify the tenant has unassigned seats available in their plan pool.

3. **Just-In-Time (JIT) Provisioning:**
   - If automatic account creation fails, verify that **Enable JIT Provisioning** is toggled ON in **Security Settings**.
   - JIT requires the IdP to send `firstName`, `lastName`, and `email` assertions.

## Escalation Criteria
- Lockouts affecting Enterprise tenant Admins with no active secondary local admin: Escalate immediately to `@security-support` with priority `HIGH`.
