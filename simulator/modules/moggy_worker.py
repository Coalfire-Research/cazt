# © 2023 Coalfire
#
# Author: Rodney Beede

import json
import re
import os
import time

from modules.data_store import AnimalPen
from modules.simulation_modes_enum import SimulationMode


SCRIPT_NAME = os.path.basename(os.path.realpath(__file__))


# Static INIT section
data_store = AnimalPen(None)


def function_handler(event, context):
    print(f"[DEBUG] {SCRIPT_NAME}", end="\t")
    print(json.dumps(event, indent=4))  #debug


    # Commonly used data from the calling client to the API (i.e. the payload)
    if "body" in event and event.get("body").strip():
        request_content = json.loads(event.get("body"))  # single body pair has encoded JSON string for value
    else:
        # Body was empty so provide empty dict so we don't have to check for None a lot later
        request_content = {}


    identity_account_id = event.get("identity", {}).get("accountId")
    if not identity_account_id:
        # This should not happen unless it was misconfigured
        print("[ERROR] NO event identity accountId SEEN. Check the calling client configuration")
        return _generate_response(401, "Where do you come from?")
    elif not re.match("^[0-9]{12}$", identity_account_id):
        print(f"[ERROR] event.identity.accountId was unexpected value of {identity_account_id}")
        return _generate_response(402, "You need to pay someone to help you with identity_account_id")

    identity_username = event.get("identity", {}).get("username")
    if not identity_username:
        # This should not happen unless it was misconfigured
        print("[ERROR] NO event identity identity_username SEEN. Check the calling client configuration")
        return _generate_response(401, "What's your name?")
    elif not re.match("^[a-zA-Z0-9_-]+$", identity_username):
        print(f"[ERROR] event.identity.username was unexpected value of {identity_username}")
        return _generate_response(402, "You need to pay someone to help you with identity_username")


    iam_simulation_mode = parse_simulation_mode(identity_username, context)
    if not iam_simulation_mode:
        return _generate_response(418, "The simulator only works with client calls in the expected format. Please try setup-cli-with-iam-test-policies.py.")
    else:
        print(f"[INFO] Using simulation mode: {iam_simulation_mode}")

    api_action = event.get("resource")
    if "/createmoggy" == api_action:
        return create_moggy(request_content, identity_account_id, iam_simulation_mode)
    elif "/listMoggies" == api_action:
        return list_moggies(request_content, identity_account_id, iam_simulation_mode)
    elif "/getMoggy" == api_action:
        return get_moggy(request_content, identity_account_id, iam_simulation_mode)
    elif "/deletemoggy" == api_action:
        return delete_moggy(request_content, identity_account_id, iam_simulation_mode)
    elif "/RunMoggyActivity" == api_action:
        return run_activity_moggy(request_content, identity_account_id, iam_simulation_mode)
    elif "/petSitter" == api_action:
        return impersonation_bind_role_moggy(request_content, identity_account_id, iam_simulation_mode)
    else:
        return _generate_response(400, "Invalid API action resource")


def parse_simulation_mode(username, http_headers_from_context):
    if not username:
        print("[ERROR] unable to parse simulation mode from request")
        return None

    try:
        mode = SimulationMode(username)
    except ValueError:
        print("[ERROR] unknown simulation mode from request")
        return None

    # Dynamically set mode based on correct exploit attempt
    if (mode == SimulationMode.CLIENT_IP_ENFORCED
       and http_headers_from_context.get("X-Forwarded-For") == "256.256.256.256" ):
        mode = SimulationMode.CLIENT_IP_SPOOFED
    elif (
       http_headers_from_context.get("Upgrade")
       and "websocket" in http_headers_from_context.get("Upgrade").lower()
       and http_headers_from_context.get("Connection")
       and "upgrade" in http_headers_from_context.get("Connection").lower()
       ):
        mode = SimulationMode.HTTP_101

    return mode


def create_moggy(request_content, identity_account_id, iam_simulation_mode):
    if not request_content:
        return _generate_response(400, "Request body was missing or empty")

    # A minimum sanity check, but not doing authZ yet
    new_name = request_content.get("Name")
    if not new_name or not new_name.strip():
        return _generate_response(400, "Invalid or missing Name")

    # Not trusted at this point, may be overridden later too
    new_actlogobjstor = request_content.get("ActivityLogObjectStorage")
    if not new_actlogobjstor or not new_actlogobjstor.strip():
        return _generate_response(400, "Invalid or missing ActivityLogObjectStorage")


    # Not trusted at this point, may be overridden later too
    arn = "arn:cloud:cazt:" + "us-texas-9" + ":" + identity_account_id + ":" + new_name


    if iam_simulation_mode == SimulationMode.ALLOW_ALL_SAME_ACCOUNT:
        # Enforce that param is correctly formatted
        if not re.match("^[a-zA-Z0-9_-]+$", new_name):
            return _generate_response(400, "Name may only have a-z, A-Z, 0-9, _, or -")

        if not re.match("^[a-zA-Z0-9._-]+$", new_actlogobjstor):
            return _generate_response(400, "ActivityLogObjectStorage may only have a-z, A-Z, 0-9, ., _, or -")
    elif iam_simulation_mode == SimulationMode.QA_SPECIFIC_API_RESOURCES:
        if "MyMoggy" != new_name:
            return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")

        if f"moggylitterbox-{identity_account_id}" != new_actlogobjstor:
            return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {new_actlogobjstor}")
    elif iam_simulation_mode == SimulationMode.QA_API_WILDCARD_REQUIRED:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CROSS_TENANT_ATTACK:
        # Enforce that param is correctly formatted
        if not re.match("^[a-zA-Z0-9_-]+$", new_name):
            return _generate_response(400, "Name may only have a-z, A-Z, 0-9, _, or -")

        if not re.match("^[a-zA-Z0-9._-]+$", new_actlogobjstor):
            return _generate_response(400, "ActivityLogObjectStorage may only have a-z, A-Z, 0-9, ., _, or -")
    elif iam_simulation_mode == SimulationMode.SAME_ACCOUNT_ATTACK:
        if "OnlyUsersMoggy" != new_name:
            return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")

        if "moggylitterbox-OnlyUsers" != new_actlogobjstor:
            return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {new_actlogobjstor}")
    elif iam_simulation_mode == SimulationMode.DENY_EXPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_IMPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_ENFORCED:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_SPOOFED:
        # Enforce that param is correctly formatted
        if not re.match("^[a-zA-Z0-9_-]+$", new_name):
            return _generate_response(400, "Name may only have a-z, A-Z, 0-9, _, or -")

        if not re.match("^[a-zA-Z0-9._-]+$", new_actlogobjstor):
            return _generate_response(400, "ActivityLogObjectStorage may only have a-z, A-Z, 0-9, ., _, or -")
    elif iam_simulation_mode == SimulationMode.IMPERSONATION:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HIERARCHICAL:
        return _generate_response(403, f"User is not authorized to call cazt:CreateMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HTTP_101:
        return _generate_response(501, "WebSockets not implemented for this particular API call")
    else:
        # Should not occur as parse_simulation_mode should have kicked out earlier
        raise NotImplementedError("iam_simulation_mode was of unmatched type")


    new_item = {
        "Arn": arn,
        "Description": request_content.get("Description"),
        "CreatedAt": int(time.time()),  # Do not care about Decimal precision
        "ActivityLogObjectStorage": new_actlogobjstor
    }

    try:
        data_store.store(arn, new_item, False)
    except LookupError:
        return _generate_response(409, "Duplicate name already exists")

    moggy = new_item
    moggy["Name"] = new_name  # Add JSON key-value pair element just for API response
    return _generate_response(200, json.dumps(moggy, indent=5))


def list_moggies(request_content, identity_account_id, iam_simulation_mode):
    # request_content should be just {} but we have it here for possible future usage (i.e. filters)

    # authZ encoded filter
    arn_prefix = "arn:cloud:cazt:" + "us-texas-9" + ":" + identity_account_id + ":"

    if iam_simulation_mode == SimulationMode.ALLOW_ALL_SAME_ACCOUNT:
        pass
    elif iam_simulation_mode == SimulationMode.QA_SPECIFIC_API_RESOURCES:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.QA_API_WILDCARD_REQUIRED:
        pass
    elif iam_simulation_mode == SimulationMode.CROSS_TENANT_ATTACK:
        pass
    elif iam_simulation_mode == SimulationMode.SAME_ACCOUNT_ATTACK:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.DENY_EXPLICIT:
        pass
    elif iam_simulation_mode == SimulationMode.DENY_IMPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_ENFORCED:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_SPOOFED:
        pass
    elif iam_simulation_mode == SimulationMode.IMPERSONATION:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.HIERARCHICAL:
        return _generate_response(403, f"User is not authorized to call cazt:ListMoggies on resource {arn_prefix}*")
    elif iam_simulation_mode == SimulationMode.HTTP_101:
        arn_prefix = None
        pass
    else:
        # Should not occur as parse_simulation_mode should have kicked out earlier
        raise NotImplementedError("iam_simulation_mode was of unmatched type")


    # Collect all the matching items
    my_litter = data_store.list(arn_prefix)

    clowder = dict()
    clowder["Clowder"] = my_litter

    return _generate_response(200, json.dumps(clowder, indent=5))


def get_moggy(request_content, identity_account_id, iam_simulation_mode):
    # A minimum sanity check, but input validation authZ is based on iam_simulation_mode
    existing_name = request_content.get("Name")  # not yet authZ trusted
    if not existing_name or not existing_name.strip():
        return _generate_response(400, "Invalid or missing Name")

    # authZ encoded filter (not yet trusted)
    arn = "arn:cloud:cazt:" + "us-texas-9" + ":" + identity_account_id + ":" + existing_name


    if iam_simulation_mode == SimulationMode.ALLOW_ALL_SAME_ACCOUNT:
        # Enforce that param is correctly formatted
        if not re.match("^[a-zA-Z0-9_-]+$", existing_name):
            return _generate_response(400, "Name may only have a-z, A-Z, 0-9, _, or -")
    elif iam_simulation_mode == SimulationMode.QA_SPECIFIC_API_RESOURCES:
        if "MyMoggy" != existing_name:
            return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.QA_API_WILDCARD_REQUIRED:
        return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CROSS_TENANT_ATTACK:
        if existing_name.startswith("arn:"):
            arn = existing_name
    elif iam_simulation_mode == SimulationMode.SAME_ACCOUNT_ATTACK:
        if "OnlyUsersMoggy" != existing_name:
            return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_EXPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_IMPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_ENFORCED:
        return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_SPOOFED:
        pass
    elif iam_simulation_mode == SimulationMode.IMPERSONATION:
        return _generate_response(403, f"User is not authorized to call cazt:GetMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HIERARCHICAL:
        pass
    elif iam_simulation_mode == SimulationMode.HTTP_101:
        return _generate_response(501, "WebSockets not implemented for this particular API call")
    else:
        # Should not occur as parse_simulation_mode should have kicked out earlier
        raise NotImplementedError("iam_simulation_mode was of unmatched type")


    try:
        matching_moggy = data_store.retrieve(arn)
    except KeyError:
        return _generate_response(404, f"Did not find {arn}")

    return _generate_response(200, json.dumps(matching_moggy, indent=5))


def delete_moggy(request_content, identity_account_id, iam_simulation_mode):
    # A minimum sanity check, but input validation authZ is based on iam_simulation_mode
    existing_name = request_content.get("Name")  # not yet trusted
    if not existing_name or not existing_name.strip():
        return _generate_response(400, "Invalid or missing Name")

    # authZ encoded filter, not yet trusted by authZ
    arn = "arn:cloud:cazt:" + "us-texas-9" + ":" + identity_account_id + ":" + existing_name


    if iam_simulation_mode == SimulationMode.ALLOW_ALL_SAME_ACCOUNT:
        # Enforce that param is correctly formatted
        if not re.match("^[a-zA-Z0-9_-]+$", existing_name):
            return _generate_response(400, "Name may only have a-z, A-Z, 0-9, _, or -")
    elif iam_simulation_mode == SimulationMode.QA_SPECIFIC_API_RESOURCES:
        if "MyMoggy" != existing_name:
            return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.QA_API_WILDCARD_REQUIRED:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CROSS_TENANT_ATTACK:
        pass
    elif iam_simulation_mode == SimulationMode.SAME_ACCOUNT_ATTACK:
        pass
    elif iam_simulation_mode == SimulationMode.DENY_EXPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_IMPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_ENFORCED:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_SPOOFED:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.IMPERSONATION:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HIERARCHICAL:
        return _generate_response(403, f"User is not authorized to call cazt:DeleteMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HTTP_101:
        return _generate_response(501, "WebSockets not implemented for this particular API call")
    else:
        # Should not occur as parse_simulation_mode should have kicked out earlier
        raise NotImplementedError("iam_simulation_mode was of unmatched type")


    try:
        data_store.remove(arn)
    except KeyError:
        return _generate_response(404, f"{arn} did not exist")

    response = dict()
    response["Message"] = f"Deleted {arn}"

    return _generate_response(200, json.dumps(response, indent=5))


def run_activity_moggy(request_content, identity_account_id, iam_simulation_mode):
    # A minimum sanity check, but input validation authZ is based on iam_simulation_mode
    arn = request_content.get("Arn")
    if not arn or not arn.strip():
        return _generate_response(400, "Invalid or missing ARN")

    # same account only
    expected_arn_prefix = "arn:cloud:cazt:" + "us-texas-9" + ":" + identity_account_id + ":"

    if iam_simulation_mode == SimulationMode.ALLOW_ALL_SAME_ACCOUNT:
        # Ensure same account was used
        if not arn.startswith(expected_arn_prefix):
            return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.QA_SPECIFIC_API_RESOURCES:
        # Name must match value in IAM policy
        if expected_arn_prefix + "MyMoggy" != arn:
            return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.QA_API_WILDCARD_REQUIRED:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CROSS_TENANT_ATTACK:
        all_but_last_arn_part = arn.rsplit(":", 1)[0]
        if any(character.isupper() for character in all_but_last_arn_part):
            arn = all_but_last_arn_part.lower() + ":" + arn.rsplit(":", 1)[1]
        elif not arn.startswith(expected_arn_prefix):
            return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
        else:
            pass
    elif iam_simulation_mode == SimulationMode.SAME_ACCOUNT_ATTACK:
        if expected_arn_prefix + "OnlyUsersMoggy" != arn:
            return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_EXPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.DENY_IMPLICIT:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_ENFORCED:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.CLIENT_IP_SPOOFED:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.IMPERSONATION:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HIERARCHICAL:
        return _generate_response(403, f"User is not authorized to call cazt:RunActivityMoggy on resource {arn}")
    elif iam_simulation_mode == SimulationMode.HTTP_101:
        return _generate_response(501, "WebSockets not implemented for this particular API call")
    else:
        # Should not occur as parse_simulation_mode should have kicked out earlier
        raise NotImplementedError("iam_simulation_mode was of unmatched type")


    try:
        matching_moggy = data_store.retrieve(arn)
    except KeyError:
        return _generate_response(404, f"Did not find {arn}")

    response = dict()
    response["Message"] = f"{matching_moggy['Name']} activity written to {matching_moggy['ActivityLogObjectStorage']}"

    return _generate_response(200, json.dumps(response, indent=5))


def impersonation_bind_role_moggy(request_content, identity_account_id, iam_simulation_mode):
    # A minimum sanity check, but input validation authZ is based on iam_simulation_mode
    arn = request_content.get("Arn")
    if not arn or not arn.strip():
        return _generate_response(400, "Invalid or missing ARN")

    # same account only unless exploited using a vulnerability
    expected_arn = "arn:cloud:iam:" + "us-texas-9" + ":" + identity_account_id + ":" + "CareForPets"

    all_but_last_arn_part = arn.rsplit(":", 1)[0]

    if (
        iam_simulation_mode != SimulationMode.IMPERSONATION
        and iam_simulation_mode != SimulationMode.QA_SPECIFIC_API_RESOURCES
        and iam_simulation_mode != SimulationMode.ALLOW_ALL_SAME_ACCOUNT
       ):
        # Not applicable to this API and the other policies implicitly deny
        return _generate_response(403, f"User is not authorized to call cazt:PetSitter on resource {arn}")

    if arn == expected_arn:
        pass
    elif (
            iam_simulation_mode == SimulationMode.IMPERSONATION
            and any(character.isupper() for character in all_but_last_arn_part)
         ):
        arn = all_but_last_arn_part.lower() + ":" + arn.rsplit(":", 1)[1]
        pass
    else:
        return _generate_response(403, f"User is not authorized to call cazt:PetSitter on resource {arn}")


    response = dict()
    response["Message"] = f"{identity_account_id} using impersonation {arn}"
    return _generate_response(200, json.dumps(response, indent=5))


def _generate_response(status_code, body):
    return {
        "statusCode": status_code,
        "body": body,
        "headers": {
            "Content-Type": "application/json"
        }
    }
