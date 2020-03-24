import requests

import config


def get_service_access_token():
    response = requests.post(
        config.token_url,
        data = {
            "grant_type": "client_credentials",
            "client_id": config.client_id,
            "client_secret": config.client_secret
        },
    )

    if response.status_code == 200:
        token_info = response.json()

        if "access_token" in token_info:
            return token_info["access_token"]
        else:
            return None
    else:
        return None
