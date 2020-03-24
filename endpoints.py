import cgi
import json
import os
import sys

import config
import resource_database
from cgi_utilities import end_with_success, end_with_status
from roles import get_authorized_roles, get_all_roles, create_role


def get_all_questionnaires():
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    all_questionnaires = resource_database.list_questionnaires()

    if "all" in authorized_roles:
        end_with_success(all_questionnaires)
    else:
        authorized_questionnaires = list(set.intersection(
            set(all_questionnaires),
            set(authorized_roles)
        ))
        end_with_success(authorized_questionnaires)


def get_questionnaire_responses(questionnaire_name):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        resource = resource_database.read_questionnaire_responses(questionnaire_name)
        end_with_success(resource)
    else:
        end_with_status(403)


def create_questionnaire():
    authorized_roles = get_authorized_roles()
    if "all" not in authorized_roles:
        end_with_status(403)
    
    form = cgi.FieldStorage()
    questionnaire_name = form.getfirst("questionnaireName")

    # TODO sanitize name

    if not questionnaire_name:
        end_with_status(400)

    all_questionnaires = resource_database.list_questionnaires()
    if questionnaire_name in all_questionnaires or questionnaire_name == "all":
        end_with_status(409)

    new_questionnaire = {
        "key": questionnaire_name,
        "place": "",
        "avatar": "",
        "date": "",
        "labels": {},
        "showBackButton": True,
        "name": "",
        "registration": []
    }

    resource_database.write_questionnaire(questionnaire_name, new_questionnaire)
    resource_database.create_collection([], questionnaire_name)
    resource_database.create_collection([questionnaire_name], "emails")
    resource_database.create_collection([questionnaire_name], "responses")

    create_role(questionnaire_name)

    end_with_success(None)

def put_questionnaire(questionnaire_name):
    input_data = json.load(sys.stdin)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)


    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        resource_database.write_questionnaire(questionnaire_name, input_data)
        end_with_status(200)
    else:
        end_with_status(403)

def get_questionnaire_labels (questionnaire_name):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_name)
        labels = questionnaire["labels"]
        end_with_success(labels)
    else:
        end_with_status(403)


def patch_questionnaire_labels (questionnaire_name):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_name)

        form = cgi.FieldStorage()

        possibleLabels = [
            "headline",
            "submit",
            "abort",
            "back",
            "submitQuestion",
            "errorInvalidForm",
            "errorDuringSubmission",
            "registrationSuccessful"
        ]

        for label in possibleLabels:
            if form.getfirst(label):
                questionnaire["labels"][label] = form.getfirst(label)
        
        resource_database.write_questionnaire(questionnaire_name, questionnaire)
        end_with_success(None)
    else:
        end_with_status(403)


def get_questionnaire_emails (questionnaire_name):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        emails = resource_database.read_questionnaire_emails(questionnaire_name)
        end_with_success(emails)
    else:
        end_with_status(403)


def patch_questionnaire_email (questionnaire_name, language):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        form = cgi.FieldStorage()

        newLanguage = form.getfirst("language", language)
        subject = form.getfirst("subject", "")
        senderAddress = form.getfirst("senderAddress", "")
        ccRecipient = form.getfirst("ccRecipient", "")
        text = form.getfirst("text", "")

        resource_database.write_questionnaire_email(questionnaire_name, newLanguage, {
            "subject": subject,
            "senderAddress": senderAddress,
            "ccRecipient": ccRecipient,
            "text": text.replace("\r\n", "\n")
        })

        if language != newLanguage:
            resource_database.delete_questionnaire_email(questionnaire_name, language)

        end_with_success(None)
    else:
        end_with_status(403)


def delete_questionnaire_email (questionnaire_name, language):
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_name in authorized_roles:
        resource_database.delete_questionnaire_email(questionnaire_name, language)
        end_with_success(None)
    else:
        end_with_status(403)
        

def get_password ():
    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)
    else:
        end_with_success(config.password)


def post_questionnaire_response (questionnaire_name):
    pass
