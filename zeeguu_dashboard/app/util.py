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

