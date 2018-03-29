import json

import flask
import requests

path = "http://51.15.89.64:9001/"
#path = "http://0.0.0.0:9001/"


def load_classes():
    returned_class_infos_string = api_get("get_classes").text
    returned_class_infos = json.loads(returned_class_infos_string)
    classes = returned_class_infos
    return classes

def load_students(class_id):
    returned_student_infos_string = api_get("get_users_from_class/"+str(class_id)).text
    returned_student_infos = json.loads(returned_student_infos_string)
    students = returned_student_infos
    return students

def load_user_data(user_id, filtered = True):
    stats_json = api_get("get_user_stats/"+str(user_id)).text
    stats = json.loads(stats_json)
    return stats

def filter_user_bookmarks(dict):
    word_string = " "
    for day in dict:
        for bookmark in day["bookmarks"]:
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
    requests.post(path+function, data=package, params=params)


def api_get(function):
    params = {
        'session': flask.session['sessionID']
    }
    returned = requests.get(path+function, params = params)
    return returned


