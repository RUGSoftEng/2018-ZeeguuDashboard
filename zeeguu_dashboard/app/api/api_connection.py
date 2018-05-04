import traceback

import flask
import requests
from requests import Response

from app import app


# This file contains the functions responsible for making calls to the Zeeguu server.


def api_post(path, package=None):
    _api_call('post', path=path, package=package)


def api_get(path):
    return _api_call('get', path=path)


def _api_call(func, path, package=None):
    params = {
        'session': flask.session['sessionID']
    }
    returned = None

    try:
        if func is 'get':
            returned = requests.get(app.config['API_PATH'] + path, params=params)
        else:
            returned = requests.post(app.config['API_PATH'] + path, data=package, params=params)
        if returned.status_code > 399:
            print('API call status code:',returned.status_code)
    except Exception:
        print(traceback.format_exc())
        raise Exception("Exception while performing request.")

    return returned



