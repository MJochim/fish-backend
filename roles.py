import requests

import config
from cgi_utilities import get_authentication_token
from openid_connect_utilities import get_service_access_token

def get_authorized_roles(send_401_if_unauthenticated = True):
    response = requests.post(
        config.introspection_url,
        data = {
            "token": get_authentication_token(send_401_if_unauthenticated),
            "client_id": config.client_id,
            "client_secret": config.client_secret
        },
        verify = config.tls_verify_server_certificates,
    )

    if response.status_code == 200:
        token_info = response.json()

        if "active" not in token_info or token_info["active"] == False:
            return []
        if "resource_access" not in token_info:
            return []
        if config.frontend_client_id not in token_info["resource_access"]:
            return []
        if "roles" not in token_info["resource_access"][config.frontend_client_id]:
            return []

        return token_info["resource_access"][config.frontend_client_id]["roles"]
    else:
        return []

def get_all_roles():
    service_access_token = get_service_access_token()

    response = requests.get(
        config.keycloak_realm_api_url + "/clients/" + config.frontend_client_uuid + "/roles",
        headers = {
            "Authorization": "Bearer " + service_access_token
        },
        verify = config.tls_verify_server_certificates,
    )

    if response.status_code == 200:
        role_list = response.json()
        return role_list
    else:
        return []
        

def create_role(role_name):
    service_access_token = get_service_access_token()

    response = requests.post(
        config.keycloak_realm_api_url + "/clients/" + config.frontend_client_uuid + "/roles",
        headers = {
            "Authorization": "Bearer " + service_access_token
        },
        verify = config.tls_verify_server_certificates,
        json = {
            "name": role_name
        }
    )

    return response.status_code
        

def delete_role(role_name):
    service_access_token = get_service_access_token()

    response = requests.delete(
        config.keycloak_realm_api_url + "/clients/" + config.frontend_client_uuid + "/roles/" + role_name,
        headers = {
            "Authorization": "Bearer " + service_access_token
        },
        verify = config.tls_verify_server_certificates,
    )

    return response.status_code
