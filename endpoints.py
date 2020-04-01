import cgi
import datetime
import json
import os
import sys

import config
import resource_database
from cgi_utilities import end_with_success, end_with_status
from email_utilities import send_email
from roles import get_authorized_roles, get_all_roles, create_role, delete_role


def get_all_questionnaires():
    authorized_roles = get_authorized_roles(False)

    all_questionnaires = resource_database.list_questionnaires()

    response = []

    for current_questionnaire_key in all_questionnaires:
        current_questionnaire_data = resource_database.read_questionnaire(current_questionnaire_key)

        public = current_questionnaire_data["public"]
        admin = (current_questionnaire_key in authorized_roles) or ("all" in authorized_roles)

        if public or admin:
            response.append({
                "key": current_questionnaire_key,
                "public": public,
                "admin": admin
            })

    end_with_success(response)


def get_questionnaire_responses(questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        resource = resource_database.read_questionnaire_responses(questionnaire_key)
        end_with_success(resource)
    else:
        end_with_status(403)


def create_questionnaire():
    authorized_roles = get_authorized_roles()
    if "all" not in authorized_roles:
        end_with_status(403)
    
    form = cgi.FieldStorage()
    questionnaire_key = form.getfirst("questionnaireKey")

    if not questionnaire_key:
        end_with_status(400)

    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    all_questionnaires = resource_database.list_questionnaires()
    if questionnaire_key in all_questionnaires or questionnaire_key == "all":
        end_with_status(409)

    new_questionnaire = {
        "key": questionnaire_key,
        "name": "",
        "pictureUrl": "",
        "labels": {},
        "registration": []
    }

    resource_database.write_questionnaire(questionnaire_key, new_questionnaire)
    resource_database.create_collection([], questionnaire_key)
    resource_database.create_collection([questionnaire_key], "emails")
    resource_database.create_collection([questionnaire_key], "responses")

    create_role(questionnaire_key)

    end_with_success(None)

def put_questionnaire(questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    input_data = json.load(sys.stdin)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)


    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        resource_database.write_questionnaire(questionnaire_key, input_data)
        end_with_status(200)
    else:
        end_with_status(403)

def get_questionnaire (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles(False)

    questionnaire = resource_database.read_questionnaire(questionnaire_key)

    if "all" in authorized_roles or questionnaire_key in authorized_roles or questionnaire["public"]: 
        end_with_success(questionnaire)
    else:
        end_with_status(403)

def delete_questionnaire (questionnaire_key):
    if questionnaire_key == "all" or not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        resource_database.delete_questionnaire(questionnaire_key)
        delete_role(questionnaire_key)

        end_with_success(None)
    else:
        end_with_status(403)


def get_questionnaire_labels (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_key)
        labels = questionnaire["labels"]
        end_with_success(labels)
    else:
        end_with_status(403)


def patch_questionnaire_labels (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_key)

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
            if label in form:
                questionnaire["labels"][label] = form.getfirst(label)
        
        resource_database.write_questionnaire(questionnaire_key, questionnaire)
        end_with_success(None)
    else:
        end_with_status(403)


def get_questionnaire_properties (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_key)
        properties = {
            "name": questionnaire["name"],
            "pictureUrl": questionnaire["pictureUrl"],
            "public": questionnaire["public"]
        }
        end_with_success(properties)
    else:
        end_with_status(403)


def patch_questionnaire_properties (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        questionnaire = resource_database.read_questionnaire(questionnaire_key)

        form = cgi.FieldStorage()

        possibleProperties = [
            "name",
            "pictureUrl",
            "public"
        ]

        booleanProperties = [
            "public"
        ]

        for property in possibleProperties:
            if property in form:
                if property in booleanProperties:
                    string_value = form.getfirst(property)
                    if string_value == "true":
                        questionnaire[property] = True
                    else:
                        questionnaire[property] = False
                else:
                    questionnaire[property] = form.getfirst(property)
        
        resource_database.write_questionnaire(questionnaire_key, questionnaire)
        end_with_success(None)
    else:
        end_with_status(403)


def get_questionnaire_emails (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        emails = resource_database.read_questionnaire_emails(questionnaire_key)
        end_with_success(emails)
    else:
        end_with_status(403)


def patch_questionnaire_email (questionnaire_key, language):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    if not resource_database.is_valid_resource_name(language):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        form = cgi.FieldStorage()

        newLanguage = form.getfirst("language", language)
        subject = form.getfirst("subject", "")
        senderAddress = form.getfirst("senderAddress", "")
        ccRecipient = form.getfirst("ccRecipient", "")
        text = form.getfirst("text", "")

        if not resource_database.is_valid_resource_name(newLanguage):
            end_with_status(400)

        resource_database.write_questionnaire_email(questionnaire_key, newLanguage, {
            "subject": subject,
            "senderAddress": senderAddress,
            "ccRecipient": ccRecipient,
            "text": text.replace("\r\n", "\n")
        })

        if language != newLanguage:
            resource_database.delete_questionnaire_email(questionnaire_key, language)

        end_with_success(None)
    else:
        end_with_status(403)


def delete_questionnaire_email (questionnaire_key, language):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    if not resource_database.is_valid_resource_name(language):
        end_with_status(400)

    authorized_roles = get_authorized_roles()
    if len(authorized_roles) == 0:
        end_with_status(403)

    if "all" in authorized_roles or questionnaire_key in authorized_roles:
        resource_database.delete_questionnaire_email(questionnaire_key, language)
        end_with_success(None)
    else:
        end_with_status(403)
        

def post_questionnaire_response (questionnaire_key):
    if not resource_database.is_valid_resource_name(questionnaire_key):
        end_with_status(400)

    input_data = json.load(sys.stdin)

    if "ContactLanguage" in input_data:
        if not resource_database.is_valid_resource_name(input_data["ContactLanguage"]):
            end_with_status(400)

    if "conferenceKey" in input_data:
        if not resource_database.is_valid_resource_name(input_data["conferenceKey"]):
            end_with_status(400)

    input_data["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # TODO Add IP and browser? Only possible if we notify the users

    resource_database.write_questionnaire_response(questionnaire_key, input_data)

    # Send confirmation email
    if config.smtp_host:
        if "ContactLanguage" in input_data:
            contact_language = input_data["ContactLanguage"][-2:]
            conference_to_extract_email_from = input_data["conferenceKey"][0:-2] + contact_language
        else:
            conference_to_extract_email_from = input_data["conferenceKey"]

        # The language feature was based on a brain fart. We therefore hardcode "" as language here.
        email_info = resource_database.read_questionnaire_email(conference_to_extract_email_from, "")

        recipient_address = input_data["Email"]

        send_email(
            email_info["senderAddress"],
            recipient_address,
            email_info["ccRecipient"],
            email_info["subject"],
            email_info["text"]
        )

    end_with_success(input_data)
