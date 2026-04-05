# 04 - Private Access Mode and Application Hardening

## Overview

This document covers the configuration of Private Access mode in SAP IAS and its role in enterprise application hardening. Private Access mode is a mandatory control for any IAS application operating in a high-security environment, including IL4, IL5, FedRAMP High, and SAP NS2 boundary deployments.

---

## What Private Access Mode Does

By default, IAS applications can allow public or self-registration access. In enterprise environments, this is not acceptable. Private Access mode enforces the following:

- Self-registration is disabled — users cannot create their own accounts
- Only users explicitly provisioned into the IAS tenant are permitted to authenticate
- Authentication via a federated corporate IdP alone is not sufficient — the user must also exist as a provisioned record in IAS
- Access is denied at the application level for any user not meeting both conditions

This creates a strict two-gate model: the user must be known to IAS AND must belong to an authorized group.

---

## Applications Configured in This Lab

| Application | Type | Protocol | Private Access |
|---|---|---|---|
| BPS-Security-Lab | SAP BTP Solution | SAML 2.0 | Enabled |
| ServiceNow-Production | SAP BTP Solution | SAML 2.0 | Enabled |

---

## Step 1 - Create the Application

1. In IAS Admin Console, navigate to **Applications & Resources** > **Applications**
2. Click **Create**
3. Configure:

| Field | Value |
|---|---|
| Display Name | BPS-Security-Lab |
| Type | SAP BTP Solution |
| Organization ID | global |
| Protocol Type | SAML 2.0 |
| Home URL | (configured per application) |

4. Click **Create**

---

## Step 2 - Enable Private Access Mode

1. Open the application
2. Navigate to the **Authentication and Access** tab
3. Locate the **User Access** setting
4. Set to **Private**
5. Save

Private mode ensures that users who successfully authenticate via Okta but are not provisioned in IAS will be denied access at the application boundary.

---

## Step 3 - Configure SAML Trust

1. Navigate to the **Trust** tab within the application
2. Click **Configure Trust Manually** or load from metadata URL
3. Enter the Service Provider endpoints:

For BPS-Security-Lab (IAS as IdP):
- The ACS URL and Entity ID point back to the IAS tenant itself since IAS is acting as both broker and IdP in this configuration

For ServiceNow-Production (ServiceNow as SP):

| Field | Value |
|---|---|
| Entity ID | https://dev373443.service-now.com |
| Single Sign-On URL (ACS) | https://dev373443.service-now.com/navpage.do |

4. Save

---

## Step 4 - Enable Corporate IdP Federation

1. Navigate to the **Trust** tab
2. Enable: **Allow logon with all configured corporate identity providers**
3. This routes authentication through Okta for all users attempting to access the application

---

## Security Design Notes

**Why Private Access mode is non-negotiable in high-security environments:**

Without Private Access mode, a user who exists in Okta could potentially authenticate to an IAS-connected application without being explicitly provisioned or authorized in IAS. This creates an access governance gap that violates least-privilege principles and NIST 800-53 AC-2 (Account Management) controls.

With Private Access mode enabled:
- Every user with access is explicitly provisioned
- Every provisioned user is tied to a specific group
- Every group is explicitly authorized for specific applications
- The full access chain is auditable from provisioning event to authentication log

**Relation to IL4/IL5 compliance:**

In SAP NS2 and DoD IL5 environments, Private Access mode maps directly to the requirement for explicit user authorization prior to system access. No implicit trust, no self-service enrollment, no exceptions.

---

## Screenshots

See `assets/screenshots/` for evidence of Private Access mode configuration on both applications.

---

## References

- [Configure Application Access in IAS](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-application-access)
- [NIST 800-53 AC-2 Account Management](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
