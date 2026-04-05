# SAP BTP Identity Authentication Service (IAS) — Enterprise Security Lab

> End-to-end implementation of SAP Cloud Identity Services – Identity Authentication (IAS) on SAP Business Technology Platform (BTP), covering enterprise SSO federation, group-based access control, user lifecycle automation, and identity governance aligned to IL5/FedRAMP security standards.

---

## Overview

This repository documents and automates the configuration of SAP BTP Identity Authentication Service (IAS) as a centralized identity and access management layer for enterprise SAP and non-SAP applications — specifically in high-security, multi-tenant environments.

The lab is structured in two phases:

- **Phase 1 (Complete):** Step-by-step configuration walkthroughs with architecture context, decision rationale, and troubleshooting scenarios — mirroring real-world enterprise implementation patterns
- **Phase 2 (In Progress):** Infrastructure as Code (Terraform), Python-based SCIM API automation, and CI/CD pipeline integration for repeatable, auditable identity operations

This work reflects implementation patterns applicable to **SAP NS2**, **FedRAMP High**, and **DoD IL4/IL5** environments where identity governance, least-privilege enforcement, and audit traceability are non-negotiable requirements.

---

## Architecture

```
+------------------------------------------------------------------+
|                     SAP BTP Global Account                        |
|                                                                    |
|  +------------------------------------------------------------+   |
|  |                    BTP Subaccount (trial)                  |   |
|  |                                                            |   |
|  |   +------------------------------------------------------+ |   |
|  |   |        SAP Cloud Identity Services (IAS)              | |   |
|  |   |        https://ajnlm5lkp.trial-accounts.ondemand.com | |   |
|  |   |                                                        | |   |
|  |   |   Users | Groups | Applications | Policies | IdPs     | |   |
|  |   |                                                        | |   |
|  |   |   Connected Applications:                             | |   |
|  |   |   - BPS-Security-Lab (SAML 2.0)                      | |   |
|  |   |   - ServiceNow-Production (SAML 2.0)                 | |   |
|  |   +------------------------------------------------------+ |   |
|  +------------------------------------------------------------+   |
+------------------------------------------------------------------+
                           |
              Corporate IdP Federation
                           |
                  +------------------+
                  |   Okta (IdP)     |
                  |  trial-8974214   |
                  +------------------+
```

**Authentication and Authorization Flow:**

```
User Request
    |
    v
IAS Authentication Check
    |
    v
Okta Corporate IdP (SAML 2.0 assertion)
    |
    v
IAS Authorization Check (group membership validation)
    |
    v
Access Granted or Denied
```

Both checks must pass. Authentication without authorization results in denial.

---

## Security Design Principles

| Principle | Implementation |
|---|---|
| No self-registration | Private Access mode enforced on all IAS applications |
| Least-privilege access | Group-based RBAC — users inherit permissions from groups only |
| Identity federation | Corporate IdP remains the source of truth — no duplicate SAP accounts |
| Automatic deprovisioning | Disabling the corporate account revokes IAS access automatically |
| Tenant isolation | Multi-tenant group design prevents lateral access across boundaries |
| Audit traceability | All provisioning actions documented and logged |
| Credential governance | No shared credentials — all access scoped to individual identities |
| NIST 800-53 alignment | AC-2, AC-3, AC-6, AC-17 controls mapped in authorization model |

---

## Repository Structure

```
sap-btp-ias-homelab/
|
+-- README.md
|
+-- docs/
|   +-- 01-ias-tenant-setup.md
|   +-- 02-user-group-management.md
|   +-- 03-saml-federation-okta.md
|   +-- 04-private-access-mode.md
|   +-- 05-authorization-model.md
|   +-- 06-troubleshooting.md
|   +-- user-import.csv
|
+-- scripts/
|   +-- import-users.py
|   +-- assign-groups.py
|   +-- validate-auth.py
|   +-- requirements.txt
|
+-- terraform/
|   +-- btp-subaccount/
|       +-- main.tf
|       +-- variables.tf
|       +-- outputs.tf
|       +-- terraform.tfvars.example
|
+-- .github/
|   +-- workflows/
|       +-- validate.yml
|
+-- csv-templates/
|   +-- user-import-template.csv
|
+-- assets/
    +-- screenshots/
```

---

## Phase 1 — Configuration Walkthroughs

### Completed

- [x] IAS tenant provisioning on SAP BTP
- [x] IAS Admin Console access and navigation
- [x] User and group creation (manual and CSV bulk import)
- [x] Group-based RBAC design and assignment
- [x] Application registration (BPS-Security-Lab, ServiceNow-Production)
- [x] Private Access mode enforcement on all applications
- [x] SAML 2.0 federation with Okta as Corporate Identity Provider
- [x] Group authorization rules configured per application
- [x] ServiceNow registered as a connected application in IAS
- [x] Troubleshooting scenarios documented with screenshots

### Documentation

| File | Description |
|---|---|
| 01-ias-tenant-setup.md | BTP subaccount and IAS instance provisioning |
| 02-user-group-management.md | User lifecycle, group design, CSV import |
| 03-saml-federation-okta.md | Corporate IdP federation via SAML 2.0 |
| 04-private-access-mode.md | Application hardening and access restriction |
| 05-authorization-model.md | Group-based RBAC design and compliance mapping |
| 06-troubleshooting.md | Common failure scenarios and remediation |

---

## Phase 2 — Automation (In Progress)

### Terraform — BTP Infrastructure

Automates subaccount creation and IAS instance provisioning using the SAP BTP Terraform Provider.

```hcl
resource "btp_subaccount" "ias_lab" {
  name      = "ias-security-lab"
  subdomain = "ias-security-lab"
  region    = "us10"
}

resource "btp_subaccount_service_instance" "ias" {
  subaccount_id  = btp_subaccount.ias_lab.id
  name           = "ias-instance"
  serviceplan_id = data.btp_subaccount_service_plan.ias.id
}
```

### Python — SCIM API Automation

| Script | Description |
|---|---|
| import-users.py | Bulk user provisioning via IAS SCIM 2.0 API |
| assign-groups.py | Automated group assignment via SCIM PATCH |
| validate-auth.py | Auth flow validation and health check |

### CI/CD — GitHub Actions

Validates scripts on every push — linting, dependency checks, and dry-run execution.

---

## Lab Environment

| Component | Details |
|---|---|
| IAS Tenant | https://ajnlm5lkp.trial-accounts.ondemand.com |
| BTP Subaccount | trial |
| Corporate IdP | Okta (trial-8974214.okta.com) |
| Protocol | SAML 2.0 |
| Applications | BPS-Security-Lab, ServiceNow-Production |
| Groups | IAS_Admin, IAS_Viewer |
| Users | 6 provisioned (3 manual, 3 via CSV import) |

---

## CSV Import — Findings

During lab execution, the IAS CSV import engine rejected the groups column. The accepted format is:

```
status,firstName,lastName,mail
```

Group assignments are handled post-import via the IAS Admin Console or programmatically via the SCIM API using assign-groups.py. The csv-templates/user-import-template.csv reflects the validated format.

---

## Relation to Enterprise IAM Patterns

The patterns implemented in this lab directly apply to:

- **SAP NS2 / Sovereign Cloud** — FedRAMP High and DoD IL5 identity governance
- **ServiceNow + IAS Integration** — SSO federation between ServiceNow and SAP BTP applications
- **Multi-tenant Enterprise Environments** — organizational boundary enforcement
- **Zero Trust Architecture** — explicit verification at every access point, no implicit trust

---

## Author

**Reyanna Pitts** — Platform Engineer | IAM Specialist | ServiceNow Architect

[LinkedIn](https://www.linkedin.com/in/reyanna-pitts-269095199/) | [GitHub](https://github.com/DataDiva93) | [Portfolio](https://www.bpscloud.io/) | [Data Divas](https://www.datadivas.org)

> "If I am going to talk about it in an interview, I want to have actually built it first."

---

## References

- [SAP Cloud Identity Services Documentation](https://help.sap.com/docs/cloud-identity-services)
- [SAP BTP Terraform Provider](https://registry.terraform.io/providers/SAP/btp/latest/docs)
- [IAS SCIM API Reference](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/scim-rest-api)
- [SAML 2.0 Federation Configuration](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-trust-with-saml-2-0-corporate-identity-provider)
- [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [SAP BTP Cockpit](https://account.hana.ondemand.com)
