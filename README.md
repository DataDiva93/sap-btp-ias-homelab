# SAP BTP Identity Authentication Service (IAS) — Enterprise Security Lab

> End-to-end implementation of SAP Cloud Identity Services – Identity Authentication (IAS) on SAP Business Technology Platform (BTP), covering enterprise SSO federation, group-based access control, user lifecycle automation, and identity governance aligned to IL5/FedRAMP security standards.

---

## Overview

This repository documents and automates the configuration of SAP BTP Identity Authentication Service (IAS) as a centralized identity and access management layer for enterprise SAP applications — specifically in high-security, multi-tenant environments.

The lab is structured in two phases:

- **Phase 1 (Documentation):** Step-by-step configuration walkthroughs with architecture context, decision rationale, and troubleshooting scenarios — mirroring real-world enterprise implementation patterns
- **Phase 2 (Automation):** Infrastructure as Code (Terraform), Python-based SCIM API automation, and CI/CD pipeline integration for repeatable, auditable identity operations

This work reflects implementation patterns applicable to **SAP NS2**, **FedRAMP High**, and **DoD IL4/IL5** environments where identity governance, least-privilege enforcement, and audit traceability are non-negotiable requirements.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SAP BTP Global Account                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    BTP Subaccount                        │    │
│  │                                                          │    │
│  │   ┌──────────────────────────────────────────────────┐  │    │
│  │   │        SAP Cloud Identity Services (IAS)          │  │    │
│  │   │                                                    │  │    │
│  │   │  ┌─────────────┐     ┌──────────────────────────┐ │  │    │
│  │   │  │  IAS Tenant  │     │   IAS Admin Console      │ │  │    │
│  │   │  │              │     │   /admin                 │ │  │    │
│  │   │  │  Users       │     │                          │ │  │    │
│  │   │  │  Groups      │     │   - User Management      │ │  │    │
│  │   │  │  Applications│     │   - App Configuration    │ │  │    │
│  │   │  │  Policies    │     │   - IdP Federation       │ │  │    │
│  │   │  └──────┬───────┘     └──────────────────────────┘ │  │    │
│  │   │         │                                           │  │    │
│  │   └─────────┼───────────────────────────────────────────┘  │    │
│  │             │                                               │    │
│  └─────────────┼───────────────────────────────────────────────┘    │
│                │                                                      │
└────────────────┼──────────────────────────────────────────────────────┘
                 │
     ┌───────────┴────────────┐
     │                        │
┌────▼────────┐      ┌────────▼────────┐
│  Corporate   │      │  Partner / Ext  │
│  IdP (Okta)  │      │  IdP (SAML/OIDC)│
│              │      │                 │
│  Employees   │      │  Suppliers      │
│  authenticate│      │  authenticate   │
│  via SSO     │      │  via federation │
└─────────────-┘      └─────────────────┘
```

**Authentication & Authorization Flow:**

```
User Request → IAS (Authentication Check) → Corporate IdP → 
IAS (Authorization Check: Group Membership) → Token Issued → 
Application Access Granted
```

Both checks must succeed. Authentication without authorization = denied.

---

## Security Design Principles

This lab is designed around the following enterprise security requirements — consistent with IL5/FedRAMP High and SAP NS2 compliance standards:

| Principle | Implementation |
|---|---|
| **No self-registration** | Private access mode enforced on all IAS applications |
| **Least-privilege access** | Group-based RBAC — users inherit permissions from groups, not direct assignments |
| **Identity federation** | Corporate IdP remains the source of truth — no duplicate SAP-specific accounts |
| **Automatic deprovisioning** | Disabling the corporate account revokes IAS access automatically |
| **Tenant isolation** | Multi-tenant group design prevents lateral access across organizational boundaries |
| **Audit traceability** | All provisioning actions documented and logged |
| **Credential governance** | No shared credentials — all access scoped to individual identities |

---

## Repository Structure

```
sap-btp-ias-homelab/
│
├── README.md                          ← You are here
│
├── docs/                              ← Phase 1: Step-by-step walkthroughs
│   ├── 01-ias-tenant-setup.md         ← BTP subaccount + IAS instance provisioning
│   ├── 02-user-group-management.md    ← User lifecycle, group design, CSV import
│   ├── 03-saml-federation-okta.md     ← Corporate IdP federation via SAML 2.0
│   ├── 04-private-access-mode.md      ← Application hardening + access restriction
│   ├── 05-authorization-model.md      ← Group-based RBAC design patterns
│   └── 06-troubleshooting.md          ← Common failure scenarios + remediation
│
├── terraform/                         ← Phase 2: Infrastructure as Code
│   └── btp-subaccount/
│       ├── main.tf                    ← BTP subaccount + IAS instance provisioning
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
│
├── scripts/                           ← Phase 2: Identity automation via SCIM API
│   ├── import-users.py                ← Bulk user provisioning via IAS SCIM API
│   ├── assign-groups.py               ← Automated group assignment
│   ├── validate-auth.py               ← Auth flow validation + health check
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── validate.yml               ← CI: lint + test scripts on push
│
├── csv-templates/
│   └── user-import-template.csv       ← IAS bulk user import template
│
└── assets/
    └── screenshots/                   ← Lab walkthrough evidence
```

---

## Phase 1 — Configuration Walkthroughs

### Completed
- [ ] IAS tenant provisioning on BTP
- [ ] IAS Admin Console access and navigation
- [ ] User and group creation
- [ ] CSV bulk user import
- [ ] Application registration in IAS
- [ ] Private access mode enforcement
- [ ] SAML 2.0 federation with Okta (Corporate IdP)
- [ ] Attribute mapping configuration
- [ ] End-to-end authentication flow validation
- [ ] Troubleshooting: auth success / access denied scenarios

### In Progress
- [ ] Multi-tenant group isolation design
- [ ] Partner organization IdP federation
- [ ] Access certification and audit log review

---

## Phase 2 — Automation (In Development)

### Terraform — BTP Infrastructure
Automates subaccount creation and IAS instance provisioning using the [SAP BTP Terraform Provider](https://registry.terraform.io/providers/SAP/btp/latest/docs).

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
Automates user provisioning, group assignment, and access validation against the IAS SCIM 2.0 API — eliminating manual CSV imports for ongoing lifecycle management.

```python
# scripts/import-users.py
import requests

def provision_user(tenant_url, token, user_data):
    """
    Provision a user via IAS SCIM 2.0 API
    POST /scim/Users
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/scim+json"
    }
    response = requests.post(
        f"{tenant_url}/scim/Users",
        headers=headers,
        json=user_data
    )
    return response.json()
```

### CI/CD — GitHub Actions
Validates scripts on every push — linting, dependency checks, and dry-run execution against a test IAS tenant.

```yaml
# .github/workflows/validate.yml
name: Validate IAS Scripts
on: [push, pull_request]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Lint
        run: flake8 scripts/
      - name: Run validation
        run: python scripts/validate-auth.py --dry-run
```

---

## Key Concepts Reference

| Term | Description |
|---|---|
| **IAS** | SAP Cloud Identity Services – Identity Authentication. Central SSO and IdP hub for SAP and non-SAP applications. |
| **BTP** | SAP Business Technology Platform. Cloud platform where IAS tenants are provisioned and managed. |
| **IAS Tenant** | Dedicated IAS instance. URL: `https://<tenant-id>.accounts.ondemand.com/admin` |
| **Corporate IdP** | Existing enterprise identity system (Okta, Azure AD, LDAP) federated to IAS via SAML 2.0 or OIDC. |
| **Private Access Mode** | IAS application setting that disables self-registration — only explicitly provisioned users can authenticate. Required for enterprise/IL5 deployments. |
| **SCIM** | System for Cross-domain Identity Management. Standard API protocol used by IAS for automated user provisioning. |
| **Group Claims** | IAS issues tokens containing group membership claims. Downstream applications validate these claims to enforce authorization. |
| **Identity Federation** | Trust relationship between IAS and a Corporate IdP — users authenticate with existing credentials, no duplicate SAP accounts required. |

---

## Relation to Enterprise IAM Patterns

The patterns implemented in this lab directly apply to:

- **SAP NS2 / Sovereign Cloud** — FedRAMP High and DoD IL5 identity governance
- **ServiceNow + IAS Integration** — SSO federation between ServiceNow and SAP BTP applications
- **Multi-tenant Enterprise Environments** — Organizational boundary enforcement across departments and partner organizations
- **Zero Trust Architecture** — Explicit verification at every access point, no implicit trust

---

## Author

**Reyanna Pitts** — Platform Engineer | IAM Specialist | ServiceNow Architect  
[LinkedIn](https://www.linkedin.com/in/reyanna-pitts-269095199/) | [GitHub](https://github.com/DataDiva93) | [Portfolio](https://www.bpscloud.io/)

> *"If I'm going to talk about it in an interview, I want to have actually built it first."*

---

## References

- [SAP Cloud Identity Services Documentation](https://help.sap.com/docs/cloud-identity-services)
- [SAP BTP Terraform Provider](https://registry.terraform.io/providers/SAP/btp/latest/docs)
- [IAS SCIM API Reference](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/scim-rest-api)
- [SAML 2.0 Federation Configuration](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-trust-with-saml-2-0-corporate-identity-provider)
- [SAP BTP Cockpit](https://account.hana.ondemand.com/)
