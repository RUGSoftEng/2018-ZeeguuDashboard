import flask
import requests

from app import app

path = "http://51.15.89.64:9001/"
#path = "http://0.0.0.0:9001/"


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


