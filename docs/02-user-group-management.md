# 02 - User and Group Management

## Overview

This document covers user lifecycle management and group-based access control within SAP IAS. IAS enforces a group membership model — users inherit application permissions through group assignments, not direct role bindings. This pattern supports least-privilege enforcement and simplifies access governance at scale.

---

## Architecture Context

Authorization in IAS is group-driven. When a user attempts to access an application, IAS validates two conditions:

1. The user's identity is authenticated
2. The user belongs to a group that is authorized for the requested application

If either condition fails, access is denied regardless of authentication success.

---

## Groups Configured

| Group Name | Display Name | Purpose |
|---|---|---|
| IAS_Admin | IAS Admin | Administrative access to platform applications |
| IAS_Viewer | IAS Viewer | Read-only access to platform applications |

---

## Step 1 - Create Groups

1. In IAS Admin Console, navigate to **Users & Authorizations** > **Groups**
2. Click **Create**
3. Enter the group name using underscore convention for technical identifiers
4. Enter the display name using space convention for human-readable labels
5. Save

Convention applied in this lab:

- Technical name (used in API and policy rules): `IAS_Admin`
- Display name (shown in UI): `IAS Admin`

---

## Step 2 - Create Users Manually

1. Navigate to **Users & Authorizations** > **Users**
2. Click **Add**
3. Complete required fields:

| Field | Convention |
|---|---|
| First Name | Descriptive first name |
| Last Name | Descriptive last name |
| Email | Unique email address per user |
| Login Name | Underscore format: `Test_Admin` |
| User Type | Employee for internal users |
| Account Activation | Set as Active for lab environments |

Users provisioned manually in this lab:

| Display Name | Email | Login Name | Group |
|---|---|---|---|
| Reyanna Pitts | datadiva93@gmail.com | — | IAS_Admin |
| Test Admin | bpscloud.identity@gmail.com | Test_Admin | IAS_Admin |
| Test Viewer | dalabmail46@gmail.com | Test_Viewer | IAS_Viewer |

---

## Step 3 - Bulk Import via CSV

IAS supports bulk user provisioning via CSV import. The accepted format is:

```
status,firstName,lastName,mail
```

The `groups` column was tested and rejected by the IAS import engine in this environment. Group assignments are handled separately after import.

CSV template is available at: `csv-templates/user-import-template.csv`

Actual import file used in this lab: `docs/user-import.csv`

Users imported via CSV:

| Display Name | Email | Status |
|---|---|---|
| Lab Admin | labuser.admin@test.com | Active |
| Lab Viewer | labuser.viewer@test.com | Active |
| Lab ReadOnly | labuser.readonly@test.com | Active |

Import procedure:

1. Navigate to **Users & Authorizations** > **Users**
2. Click **Import Users**
3. Select the CSV file
4. Review the preview — confirm user count and update count
5. Confirm import

---

## Step 4 - Assign Users to Groups

After users are created, assign each user to the appropriate group:

1. Open the user record
2. Navigate to the **Groups** tab
3. Select the target group
4. Save

Final group assignments:

| User | Group |
|---|---|
| Reyanna Pitts | IAS_Admin |
| Test Admin | IAS_Admin |
| Lab Admin | IAS_Admin |
| Test Viewer | IAS_Viewer |
| Lab Viewer | IAS_Viewer |
| Lab ReadOnly | IAS_Viewer |

---

## SCIM API Automation

Group assignments and user provisioning can be automated via the IAS SCIM 2.0 API. Scripts are available in the `scripts/` directory:

- `scripts/import-users.py` — bulk user provisioning via SCIM API
- `scripts/assign-groups.py` — automated group assignment via SCIM PATCH

---

## Screenshots

See `assets/screenshots/` for evidence of group creation, manual user creation, CSV import confirmation, and group assignments.

---

## References

- [IAS User Management Documentation](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/user-management)
- [IAS SCIM REST API](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/scim-rest-api)
