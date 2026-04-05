# 03 - SAML 2.0 Federation with Okta

## Overview

This document covers the configuration of SAML 2.0 identity federation between SAP IAS and Okta as a Corporate Identity Provider. When federation is configured, IAS delegates authentication to Okta — users authenticate with their existing Okta credentials rather than maintaining separate IAS accounts. IAS then enforces authorization based on group membership after Okta confirms the user's identity.

---

## Architecture Context

```
User Access Request
        |
        v
SAP IAS (Authentication Broker)
        |
        v
Okta (Corporate Identity Provider)
        |
   SAML Assertion
        |
        v
IAS validates assertion + group membership
        |
        v
Access granted or denied
```

This pattern eliminates duplicate user accounts, centralizes authentication policy, and ensures that revoking a user in Okta automatically revokes their access to all IAS-connected applications.

---

## Prerequisites

- Active Okta developer account (free at developer.okta.com)
- IAS tenant provisioned and accessible
- IAS application created (BPS-Security-Lab)

---

## Part 1 - Configure Okta as a SAML Service Provider

### Step 1 - Create a SAML App Integration in Okta

1. In Okta Admin Console, navigate to **Applications** > **Applications**
2. Click **Create App Integration**
3. Select **SAML 2.0**
4. Click **Next**
5. Set application name: `SAP-IAS-BPS-Lab`
6. Click **Next**

### Step 2 - Configure SAML Settings in Okta

Use the IAS tenant endpoints to populate the Okta SAML configuration:

| Okta Field | Value |
|---|---|
| Single Sign-On URL | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/acs/ajnlm5lkp.trial-accounts.ondemand.com |
| Recipient URL | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/acs/ajnlm5lkp.trial-accounts.ondemand.com |
| Destination URL | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/acs/ajnlm5lkp.trial-accounts.ondemand.com |
| Audience URI (Entity ID) | https://ajnlm5lkp.trial-accounts.ondemand.com |
| Name ID Format | EmailAddress |
| Application Username | Email |
| Default Relay State | (leave blank) |

Signing configuration applied:

| Setting | Value |
|---|---|
| Response | Signed |
| Assertion Signature | Signed |
| Signature Algorithm | RSA_SHA256 |
| Digest Algorithm | SHA256 |

### Step 3 - Retrieve Okta Metadata URL

After saving the Okta app, navigate to the **Sign On** tab and locate:

```
Metadata URL: https://trial-8974214.okta.com/app/exk11mu9xjj7JNeCW698/sso/saml/metadata
```

This URL is used in the next section to configure IAS trust.

---

## Part 2 - Configure Corporate IdP in IAS

### Step 4 - Add Okta as a Corporate Identity Provider

1. In IAS Admin Console, navigate to **Identity Providers**
2. Click **Add** > **Corporate Identity Provider**
3. Set name: `Okta-Corporate-IdP`
4. Select **Load metadata from URL**
5. Paste the Okta metadata URL:

```
https://trial-8974214.okta.com/app/exk11mu9xjj7JNeCW698/sso/saml/metadata
```

6. Click **Load** — IAS automatically imports the signing certificate, SSO endpoint, and issuer
7. Save

IAS imports the following from the Okta metadata:

| Field | Value |
|---|---|
| Single Sign-On Endpoint | https://trial-8974214.okta.com/app/trial-8974214_sapiasbpslab_1/exk11mu9xjj7JNeCW698/sso/saml |
| Issuer | http://www.okta.com/exk11mu9xjj7JNeCW698 |
| Signing Certificate | SHA-2, valid April 4 2026 to April 4 2036 |

### Step 5 - Enable Corporate IdP on the Application

1. Navigate to **Applications & Resources** > **Applications**
2. Open **BPS-Security-Lab**
3. Navigate to the **Trust** tab
4. Enable: **Allow logon with all configured corporate identity providers**
5. Save

---

## IAS Tenant Endpoints Reference

| Endpoint | URL |
|---|---|
| Entity ID | https://ajnlm5lkp.trial-accounts.ondemand.com |
| SSO (HTTP-Redirect) | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/sso/ajnlm5lkp.trial-accounts.ondemand.com |
| SSO (HTTP-POST) | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/sso/ajnlm5lkp.trial-accounts.ondemand.com |
| ACS | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/acs/ajnlm5lkp.trial-accounts.ondemand.com |
| SLO | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/idp/slo/ajnlm5lkp.trial-accounts.ondemand.com |
| Metadata | https://ajnlm5lkp.trial-accounts.ondemand.com/saml2/metadata |

---

## Key Design Decisions

**Metadata URL over manual configuration:** Loading metadata from URL ensures that certificate rotations and endpoint changes in Okta are automatically reflected in IAS without manual intervention.

**EmailAddress as Name ID Format:** Ensures the SAML assertion carries a consistent, human-readable identifier that maps cleanly to IAS user records and downstream application user fields.

**RSA_SHA256 signing:** Meets enterprise security standards and is required for IL4/IL5 and FedRAMP-aligned environments.

---

## Screenshots

See `assets/screenshots/` for evidence of the Okta SAML app configuration, IAS Corporate IdP setup, and federation trust enablement.

---

## References

- [Configure Trust with SAML 2.0 Corporate IdP](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-trust-with-saml-2-0-corporate-identity-provider)
- [Okta SAML 2.0 Documentation](https://developer.okta.com/docs/concepts/saml/)
