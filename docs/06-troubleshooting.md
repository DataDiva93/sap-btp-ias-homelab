# Troubleshooting Scenarios

## Scenario 1 — User authenticated but access denied (no group membership)

### What was changed
Removed Test Viewer user from IAS Viewer group.

### Expected behavior
User can authenticate via Identity Authentication but is 
blocked from accessing BPS-Security-Lab application because 
they have no group membership mapped to the application.

### Root cause
IAS authorization check fails — authentication succeeds at 
the IdP level but group membership validation denies access. 
This is the two-check model: authentication AND authorization 
must both pass.

### Resolution
Re-assign user to appropriate group (IAS Viewer) to restore 
access.

### Screenshot
See docs/screenshots/ for evidence of user with no group 
assignment.


## Scenario 2 — Private Access blocks user with no group assignment

### What was changed
Lab ReadOnly user exists in IAS but has no group membership 
assigned.

### Expected behavior
Even though the user exists in the system, Private Access mode 
combined with no group assignment means access to 
BPS-Security-Lab is denied.

### Root cause
Private Access mode requires explicit group membership mapped 
to the application. Existence in the tenant alone is not 
sufficient for access.

### Resolution
Assign user to appropriate group OR remove user if access 
should never be granted.

### Screenshot
See docs/screenshots/ for evidence of unprovisioned user 
with no group assignment.


## Scenario 3 — Corporate IdP federation disabled, auth failure

### What was changed
Okta Corporate Identity Provider trust disabled on 
BPS-Security-Lab application.

### Expected behavior
Authentication fails at the federation layer. IAS cannot 
route the authentication request to Okta. User receives 
an authentication error before even reaching the 
authorization check.

### Root cause
Trust relationship between IAS and Corporate IdP broken.
No fallback IdP configured. Authentication chain fails 
at the first step.

### Resolution
Re-enable Okta-Corporate-IdP trust on the application.
Verify metadata is still valid and certificate has not 
expired.

### Screenshot
See docs/screenshots/ for evidence of disabled IdP trust.