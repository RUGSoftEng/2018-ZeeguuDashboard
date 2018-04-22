import json

import flask
import requests
from app import app
path = "http://51.15.89.64:9001/"
#path = "http://0.0.0.0:9001/"


def load_user_info(user_id):
    student_info = api_get('user_info/'+str(user_id))
    return json.loads(student_info.text)

def remove_class(class_id):
    dict = {}
    api_post('remove_cohort/'+str(class_id), dict)

def load_class_info(id):
    returned_class_infos_string = api_get("cohort_info/"+str(id)).text
    returned_class_info = json.loads(returned_class_infos_string)
    class_info = returned_class_info
    return class_info

def load_classes():
    returned_class_infos_string = api_get("cohorts_info").text
    returned_class_infos = json.loads(returned_class_infos_string)
    classes = returned_class_infos
    return classes

def load_students(class_id):
    returned_student_infos_string = api_get("users_from_cohort/"+str(class_id)).text
    returned_student_infos = json.loads(returned_student_infos_string)
    students = returned_student_infos
    return students

def load_user_data(user_id, filtered = True):
    stats_json = api_get("cohort_member_bookmarks/"+str(user_id)).text
    stats = json.loads(stats_json)
    return stats

def filter_user_bookmarks(dict):
    word_string = " "
    for day in dict:
        for bookmark in day["bookmar1ks"]:
            if bookmark["from"] in word_string:
                day["bookmarks"].remove(bookmark)
            else:
                word_string = bookmark["from"]
    return dict

def verify_invite_code_exists(inv_code):

    inv_code_bool = api_get('check_invite_code/' + str(inv_code)).text
    inv_code_bool = json.loads(inv_code_bool)
    if inv_code_bool == 1:
        return False
    return True

def api_post(function, package):
    params = {
        'session':flask.session['sessionID']
    }
    requests.post(app.config['API_PATH']+function, data=package, params=params)


def api_get(function):
    params = {
        'session': flask.session['sessionID']
    }
    returned = requests.get(app.config['API_PATH']+function, params = params)
    return returned


