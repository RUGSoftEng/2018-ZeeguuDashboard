import traceback

import flask
import requests
from flask import redirect

from app import app

"""
This file contains the functions responsible for making calls to the Zeeguu server.
"""


def api_post(path, package=None, validate=True):
    """
    :param path: The requested endpoint of the Zeeguu_API.
    :param package: Any information sent to the Zeeguu_API.
    :return: Returns the response of the Zeeguu_API.
    """
    return validate_response(_api_call('post', path=path, package=package))


def api_get(path, validate=True):
    """
    :param path: The requested endpoint of the Zeeguu_API.
    :return: Returns the response from Zeeguu_API, which contains the requested information.
    """
    return validate_response(_api_call('get', path=path))


def _api_call(func, path, package=None):
    """
    :param func: Indicates whether the api call is a 'get' or a 'post'.
    :param path: The requested endpoint of the Zeeguu_API.
    :param package: Any information sent to the Zeeguu_API.
    :return: Returns a response, which contains the requested data on a 'get' call.
    """
    params = {
        'session': flask.session['sessionID']
    }
    returned = None

    try:
        if func is 'get':
            returned = requests.get(app.config['API_PATH'] + path, params=params)
        else:
            returned = requests.post(app.config['API_PATH'] + path, data=package, params=params)
    except Exception:
        print(traceback.format_exc())
        raise Exception("Exception while performing request.")

    return returned

def validate_response(response):
    if response.status_code is not 200:
        redirect("/404")
    else:
        return response