# 05 - Authorization Model and Group-Based Access Control

## Overview

This document describes the authorization model implemented across the IAS tenant in this lab. The model is built on group-based access control (GBAC) — a pattern where users inherit application permissions through group membership rather than direct role assignments. This approach is standard in enterprise identity governance and is required for compliance with NIST 800-53, FedRAMP, and SAP NS2 security boundary requirements.

---

## Authorization Architecture

IAS enforces authorization through Risk-Based Authentication rules configured at the application level. Each rule defines:

- Which users are allowed (by user type, group, IP range, or email domain)
- What authentication action to apply (allow, deny, require step-up)
- Which identity provider handles the authentication

The result is a layered access control model where authentication and authorization are evaluated as separate, sequential checks.

---

## The Two-Check Model

Every access attempt to an IAS-connected application goes through two checks:

```
Step 1 - Authentication
Is this a valid identity? Verified via Corporate IdP (Okta).

Step 2 - Authorization
Is this identity permitted to access this specific application?
Verified via IAS group membership rules.

Both checks must pass. Authentication success alone does not grant access.
```

This separation is critical for multi-tenant enterprise environments where different user populations require different access boundaries across the same identity infrastructure.

---

## Authorization Rules Configured

### BPS-Security-Lab

| Priority | Identity Provider | User Type | Group | IP Range | Action |
|---|---|---|---|---|---|
| 1 | Identity Authentication | Employee | IAS_Admin | Any | Allow |
| 2 | Identity Authentication | Employee | IAS_Viewer | Any | Allow |

### ServiceNow-Production

| Priority | Identity Provider | User Type | Group | IP Range | Action |
|---|---|---|---|---|---|
| 1 | Identity Authentication | Employee | IAS_Admin | Any | Allow |
| 2 | Identity Authentication | Employee | IAS_Viewer | Any | Allow |

---

## Group Design Principles

**Least privilege:** Users are assigned to the minimum group required for their function. No user is assigned to IAS_Admin unless administrative access is explicitly required.

**Group as policy boundary:** Groups define what a user can access, not just who they are. A user in IAS_Admin across two applications has admin access to both — group design must account for cross-application scope.

**Separation of duties:** IAS_Admin and IAS_Viewer are mutually exclusive in terms of their intended use. Assigning a user to both groups should be avoided unless a documented business justification exists.

**Cloud groups over on-premise groups:** All groups in this lab are cloud-native IAS groups. On-premise group mapping via LDAP is not configured in this environment.

---

## User-to-Group-to-Application Mapping

```
Reyanna Pitts (datadiva93@gmail.com)
  -> IAS_Admin
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)

Test Admin (bpscloud.identity@gmail.com)
  -> IAS_Admin
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)

Lab Admin (labuser.admin@test.com)
  -> IAS_Admin
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)

Test Viewer (dalabmail46@gmail.com)
  -> IAS_Viewer
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)

Lab Viewer (labuser.viewer@test.com)
  -> IAS_Viewer
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)

Lab ReadOnly (labuser.readonly@test.com)
  -> IAS_Viewer
     -> BPS-Security-Lab (Allow)
     -> ServiceNow-Production (Allow)
```

---

## Multi-Tenant Isolation

In production enterprise deployments, the authorization model extends to enforce tenant isolation — preventing lateral access between departments or partner organizations. This is achieved by:

- Creating separate groups per organizational boundary (e.g., Finance_Users, SupplyChain_Users)
- Mapping each group to only the applications that boundary is authorized for
- Ensuring no group spans organizational boundaries without explicit governance approval

This pattern directly supports SAP NS2 requirements for multi-tenant security boundary enforcement.

---

## Compliance Alignment

| Control | Implementation |
|---|---|
| NIST 800-53 AC-2 (Account Management) | All users explicitly provisioned, no self-registration |
| NIST 800-53 AC-3 (Access Enforcement) | Group-based rules enforce application-level access |
| NIST 800-53 AC-6 (Least Privilege) | Users assigned minimum required group only |
| NIST 800-53 AC-17 (Remote Access) | All access via federated IdP with enforced authentication |
| FedRAMP / DoD IL5 | Private Access mode + explicit provisioning + audit logging |

---

## Screenshots

See `assets/screenshots/` for evidence of authorization rules configured on both applications.

---

## References

- [IAS Risk-Based Authentication Rules](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-risk-based-authentication-for-an-application)
- [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
