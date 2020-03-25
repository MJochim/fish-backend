import json
import os

import config


#############################################
######## General database functions #########
#############################################

def create_collection(parent_collections, collection_name):
    parent_collections = [x + "_collection/" for x in parent_collections]
    collection_path = ''.join(parent_collections)

    path = config.data_directory + "/" + collection_path + collection_name + "_collection"

    os.mkdir(path)


def read_record(parent_collections, record_name):
    parent_collections = [x + "_collection/" for x in parent_collections]
    collection_path = ''.join(parent_collections)

    path = config.data_directory + "/" + collection_path + record_name + "_record"
    file_handle = open (path, "r")
    return json.load(file_handle)


def write_record(parent_collections, record_name, record):
    parent_collections = [x + "_collection/" for x in parent_collections]
    collection_path = ''.join(parent_collections)

    path = config.data_directory + "/" + collection_path + record_name + "_record"
    file_handle = open (path, "w")
    json.dump(record, file_handle)


def delete_record(parent_collections, record_name):
    parent_collections = [x + "_collection/" for x in parent_collections]
    collection_path = ''.join(parent_collections)

    path = config.data_directory + "/" + collection_path + record_name + "_record"
    os.remove(path)


def read_collection(parent_collections, collection_name, named = False):
    parent_collections = [x + "_collection/" for x in parent_collections]
    collection_path = ''.join(parent_collections)

    path = config.data_directory + "/" + collection_path + collection_name + "_collection"

    if named:
        records = {}
    else:
        records = []

    for entry in os.scandir(path):
        if entry.name.endswith("_record"):
            record_file = open(entry.path, "r")
            record = json.load(record_file)
            if named:
                record_name = entry.name[0:-len("_record")]
                records[record_name] = record
            else:
                records.append(record)

    return records


#############################################
######## Questionnaire-specific functions ###
#############################################

def list_questionnaires():
    questionnaires = []

    for entry in os.scandir(config.data_directory):
        if entry.name.endswith("_collection"):
            questionnaires.append(entry.name[:-len("_collection")])

    return questionnaires

def read_questionnaire(questionnaire_key):
    return read_record([], questionnaire_key)

def write_questionnaire(questionnaire_key, questionnaire):
    write_record([], questionnaire_key, questionnaire)

def read_questionnaire_emails(questionnaire_key):
    return read_collection([questionnaire_key], "emails", named = True)

def read_questionnaire_email(questionnaire_key, language):
    return read_record([questionnaire_key, "emails"], language)

def write_questionnaire_email(questionnaire_key, language, email):
    return write_record([questionnaire_key, "emails"], language, email)
    
def delete_questionnaire_email(questionnaire_key, language):
    return delete_record([questionnaire_key, "emails"], language)
    
def read_questionnaire_responses(questionnaire_key):
    return read_collection([questionnaire_key], "responses")
