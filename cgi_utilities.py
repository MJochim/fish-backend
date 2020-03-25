#!/usr/bin/python3

import json
import os
import sys
import urllib

import config


def end_with_success(result):
    print("Status: 200")
    print("Content-Type: application/json")
    print()

    print (json.dumps(result))
    sys.exit()


def end_with_status(status_code):
    print("Status: " + str(status_code))
    print()
    sys.exit()


def end_if_request_is_preflight():
    if os.environ["REQUEST_METHOD"] == "OPTIONS":
        end_with_status(200)
    

def print_headers(headers):
    for header in headers:
        print(header + ": " + headers[header])


def get_authentication_token(send_401_if_absent):
    if "HTTP_AUTHORIZATION" not in os.environ:
        if send_401_if_absent:
            end_with_status(401)
        else:
            return None

    expected_prefix = "Bearer "
    authorization_header = os.environ["HTTP_AUTHORIZATION"]

    if authorization_header[0:len(expected_prefix)] == expected_prefix:
        return(authorization_header[len(expected_prefix):])
    else:
        if send_401_if_absent:
            end_with_status(401)
        else:
            return None


def get_request_path_components():
    # REQUEST_URI contains e.g. /questionnaire-data/resources/some-conference
    # It does not actually contain a URI, but rather only a path
    request_path = os.environ["REQUEST_URI"]

    expected_path_prefix = config.base_url + "/"

    if not request_path.startswith(expected_path_prefix) :
        end_with_status(400)
    meaningful_request_path = request_path[len(expected_path_prefix):]

    path_components = meaningful_request_path.split("/")
    path_components = [urllib.parse.unquote_plus(x) for x in path_components]

    return path_components
