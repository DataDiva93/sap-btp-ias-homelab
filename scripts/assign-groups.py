"""
assign-groups.py
Automated group assignment via SAP IAS SCIM 2.0 API
BPS Cloud - SAP BTP IAS Home Lab
"""

import requests
import os
from datetime import datetime

# IAS Tenant Configuration
IAS_TENANT_URL = os.environ.get(
    "IAS_TENANT_URL",
    "https://ajnlm5lkp.trial-accounts.ondemand.com"
)
IAS_CLIENT_ID = os.environ.get("IAS_CLIENT_ID", "")
IAS_CLIENT_SECRET = os.environ.get("IAS_CLIENT_SECRET", "")

SCIM_USERS_ENDPOINT = f"{IAS_TENANT_URL}/scim/Users"
SCIM_GROUPS_ENDPOINT = f"{IAS_TENANT_URL}/scim/Groups"


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


def get_user_id(token, email):
    """
    Look up a user's SCIM ID by email address.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/scim+json"
    }
    params = {"filter": f'emails.value eq "{email}"'}
    response = requests.get(
        SCIM_USERS_ENDPOINT, headers=headers, params=params
    )
    response.raise_for_status()

    resources = response.json().get("Resources", [])
    if not resources:
        return None
    return resources[0].get("id")


def get_group_id(token, group_name):
    """
    Look up a group's SCIM ID by display name.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/scim+json"
    }
    params = {"filter": f'displayName eq "{group_name}"'}
    response = requests.get(
        SCIM_GROUPS_ENDPOINT, headers=headers, params=params
    )
    response.raise_for_status()

    resources = response.json().get("Resources", [])
    if not resources:
        return None
    return resources[0].get("id")


def assign_user_to_group(token, user_email, group_name):
    """
    Assign a user to a group via SCIM PATCH operation.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/scim+json"
    }

    user_id = get_user_id(token, user_email)
    if not user_id:
        print(f"[NOT FOUND] User: {user_email}")
        return False

    group_id = get_group_id(token, group_name)
    if not group_id:
        print(f"[NOT FOUND] Group: {group_name}")
        return False

    patch_payload = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [
            {
                "op": "add",
                "path": "members",
                "value": [{"value": user_id}]
            }
        ]
    }

    response = requests.patch(
        f"{SCIM_GROUPS_ENDPOINT}/{group_id}",
        headers=headers,
        json=patch_payload
    )

    if response.status_code in [200, 204]:
        print(f"[SUCCESS] Assigned {user_email} -> {group_name}")
        return True
    else:
        print(f"[FAILED]  {user_email} -> {group_name}: {response.text}")
        return False


def bulk_assign(assignments):
    """
    Bulk assign users to groups from a list of (email, group_name) tuples.

    Example:
        assignments = [
            ("testadmin@bpscloud.io", "IAS Admin"),
            ("testviewer@bpscloud.io", "IAS Viewer"),
        ]
    """
    print(f"\n[{datetime.now()}] Starting bulk group assignments")
    print("-" * 60)

    token = get_access_token()
    success = 0
    failed = 0

    for email, group in assignments:
        result = assign_user_to_group(token, email, group)
        if result:
            success += 1
        else:
            failed += 1

    print("-" * 60)
    print(f"Success: {success}")
    print(f"Failed:  {failed}")
    print(f"[{datetime.now()}] Assignments complete.")


if __name__ == "__main__":
    # Define your assignments here
    assignments = [
        ("bpscloud.identity@gmail.com", "IAS Admin"),
        ("dalabmail46@gmail.com", "IAS Viewer"),
        ("labuser.admin@test.com", "IAS Admin"),
        ("labuser.viewer@test.com", "IAS Viewer"),
        ("labuser.readonly@test.com", "IAS Viewer"),
    ]
    bulk_assign(assignments)
