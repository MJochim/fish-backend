#!/usr/bin/python3

import cgitb
import os


import config
if config.debug_mode:
    cgitb.enable(display = 0, logdir = config.cgi_trace_logdir, format = "plaintext")


import endpoints
from cgi_utilities import print_headers, end_if_request_is_preflight, end_with_status, get_request_path_components


print_headers(config.headers)
end_if_request_is_preflight()
request_method = os.environ["REQUEST_METHOD"]
path_components = get_request_path_components()


if len(path_components) < 1:
    end_with_status(404)

elif len(path_components) == 1 and path_components[0] == "password":
    if request_method == "GET":
        endpoints.get_password()
    else:
        end_with_status(405)

elif path_components[0] != "questionnaires":
    end_with_status(404)

elif len(path_components) == 1:
    if request_method == "GET":
        endpoints.get_all_questionnaires()
    elif request_method == "POST":
        endpoints.create_questionnaire()
    else:
        end_with_status(405)

elif len(path_components) == 2:
    questionnaire_name = path_components[1]

    if request_method == "GET":
        # return the questionnaire (and not its responses)
        end_with_status(501)
    elif request_method == "PUT":
        endpoints.put_questionnaire(questionnaire_name)
    else:
        end_with_status(405)

elif len(path_components) == 3 and path_components[2] == "responses":
    questionnaire_name = path_components[1]

    if request_method == "GET":
        endpoints.get_questionnaire_responses(questionnaire_name)
    elif request_method == "POST":
        end_with_status(501)
    else:
        end_with_status(405)

elif len(path_components) == 3 and path_components[2] == "labels":
    questionnaire_name = path_components[1]

    if request_method == "GET":
        endpoints.get_questionnaire_labels(questionnaire_name)
    elif request_method == "PATCH":
        endpoints.patch_questionnaire_labels(questionnaire_name)
    else:
        end_with_status(405)

elif len(path_components) == 3 and path_components[2] == "emails":
    questionnaire_name = path_components[1]

    if request_method == "GET":
        endpoints.get_questionnaire_emails(questionnaire_name)
    else:
        end_with_status(405)

elif len(path_components) == 4 and path_components[2] == "emails":
    questionnaire_name = path_components[1]
    language = path_components[3]

    if request_method == "PATCH":
        endpoints.patch_questionnaire_email(questionnaire_name, language)
    elif request_method == "DELETE":
        endpoints.delete_questionnaire_email(questionnaire_name, language)
    else:
        end_with_status(405)

else:
    end_with_status(404)
