"""
import-users.py
Bulk user provisioning via SAP IAS SCIM 2.0 API
BPS Cloud - SAP BTP IAS Home Lab
"""

import requests
import csv
import os
from datetime import datetime

# IAS Tenant Configuration
IAS_TENANT_URL = os.environ.get("IAS_TENANT_URL", "https://ajnlm5lkp.trial-accounts.ondemand.com")
IAS_CLIENT_ID = os.environ.get("IAS_CLIENT_ID", "")
IAS_CLIENT_SECRET = os.environ.get("IAS_CLIENT_SECRET", "")

SCIM_USERS_ENDPOINT = f"{IAS_TENANT_URL}/scim/Users"


def get_access_token():
    """
    Obtain OAuth 2.0 access token from IAS token endpoint.
    """
    token_url = f"{IAS_TENANT_URL}/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": IAS_CLIENT_ID,
        "client_secret": IAS_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json().get("access_token")


def provision_user(token, user_data):
    """
    Provision a single user via IAS SCIM 2.0 API.
    POST /scim/Users
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/scim+json"
    }

    scim_payload = {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "userName": user_data["mail"],
        "name": {
            "givenName": user_data["firstName"],
            "familyName": user_data["lastName"]
        },
        "emails": [
            {
                "value": user_data["mail"],
                "primary": True
            }
        ],
        "active": user_data["status"].lower() == "active"
    }

    response = requests.post(
        SCIM_USERS_ENDPOINT,
        headers=headers,
        json=scim_payload
    )

    return response.status_code, response.json()


def import_users_from_csv(csv_file_path):
    """
    Read users from CSV and provision each via SCIM API.
    CSV format: status,firstName,lastName,mail
    """
    print(f"\n[{datetime.now()}] Starting user import from: {csv_file_path}")
    print("-" * 60)

    token = get_access_token()
    results = {"success": [], "failed": []}

    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            status_code, response = provision_user(token, row)

            if status_code == 201:
                print(f"[SUCCESS] Created: {row['mail']}")
                results["success"].append(row["mail"])
            else:
                print(f"[FAILED]  {row['mail']} - {response.get('detail', 'Unknown error')}")
                results["failed"].append(row["mail"])

    print("-" * 60)
    print(f"Success: {len(results['success'])} users")
    print(f"Failed:  {len(results['failed'])} users")
    print(f"[{datetime.now()}] Import complete.")

    return results


if __name__ == "__main__":
    csv_path = os.path.join(os.path.dirname(__file__), "../csv-templates/user-import-template.csv")
    import_users_from_csv(csv_path)