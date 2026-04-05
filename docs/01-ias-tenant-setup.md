# 01 - IAS Tenant Setup on SAP BTP

## Overview

This document covers the provisioning and initial configuration of an SAP Cloud Identity Services - Identity Authentication (IAS) tenant on SAP Business Technology Platform (BTP). The IAS tenant serves as the central authentication and authorization layer for all applications registered in this lab.

---

## Prerequisites

- SAP BTP global account (trial or enterprise)
- BTP subaccount with administrative permissions
- Access to SAP BTP Cockpit: https://account.hana.ondemand.com

---

## Architecture Context

IAS sits between the corporate identity provider and all connected SAP and non-SAP applications. It acts as an identity broker — federating authentication requests to the appropriate corporate IdP while enforcing centralized access policies.

```
Corporate IdP (Okta) <-> IAS Tenant <-> Connected Applications
                                         - BPS-Security-Lab
                                         - ServiceNow-Production
```

---

## Step 1 - Access SAP BTP Cockpit

1. Navigate to https://account.hana.ondemand.com
2. Log in with your SAP Universal ID
3. Select your global account
4. Navigate to your target subaccount

---

## Step 2 - Verify Cloud Identity Services Entitlement

1. In the subaccount, navigate to **Entitlements**
2. Search for **Cloud Identity Services**
3. Confirm the **default** plan is entitled
4. If not present, click **Edit** and add the service plan

Each SAP BTP global account includes one free production IAS tenant and one free test IAS tenant.

---

## Step 3 - Subscribe to Cloud Identity Services

1. Navigate to **Services** > **Instances and Subscriptions**
2. Click **Create**
3. Select **Cloud Identity Services**
4. Choose plan: **default**
5. Click **Create**

Provisioning typically completes within 1 to 2 minutes.

---

## Step 4 - Activate the IAS Tenant

After provisioning, SAP sends an activation email from:

```
no-reply@accountactivation.sap.com
```

Click the activation link in that email to initialize the IAS tenant. This step is required before the Admin Console becomes accessible.

---

## Step 5 - Access the IAS Admin Console

The IAS Admin Console URL follows this format:

```
https://<tenant-id>.accounts.ondemand.com/admin
```

For this lab, the tenant URL is:

```
https://ajnlm5lkp.trial-accounts.ondemand.com/admin
```

Log in using your SAP Universal ID credentials.

---

## Lab Tenant Details

| Field | Value |
|---|---|
| Tenant URL | https://ajnlm5lkp.trial-accounts.ondemand.com |
| Admin Console | https://ajnlm5lkp.trial-accounts.ondemand.com/admin |
| Subaccount | trial |
| Plan | default |
| Status | Active |

---

## Screenshots

See `assets/screenshots/` for evidence of the provisioned IAS tenant and Admin Console access.

---

## References

- [SAP Cloud Identity Services Documentation](https://help.sap.com/docs/cloud-identity-services)
- [SAP BTP Cockpit](https://account.hana.ondemand.com)
