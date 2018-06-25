import traceback

import flask
import requests
from requests import HTTPError

from zeeguu_teacher_dashboard import app

"""
This file contains the functions responsible for making calls to the Zeeguu server.
"""


def api_post(path, package=None, raise_for_status=True):
    """
    :param path: The requested endpoint of the Zeeguu_API.
    :param package: Any information sent to the Zeeguu_API.
    :param raise_for_status: Boolean to indicate whether
    the API call should raise an exception for status a bad status code.
    :return: Returns the response of the Zeeguu_API.
    """
    return _api_call('post', path=path, package=package, raise_for_status=raise_for_status)


def api_get(path, raise_for_status=True):
    """
    :param path: The requested endpoint of the Zeeguu_API.
    :param raise_for_status: Boolean to indicate whether
    the API call should raise an exception for status a bad status code.
    :return: Returns the response from Zeeguu_API, which contains the requested information.
    """
    return _api_call('get', path=path, raise_for_status=raise_for_status)


def _api_call(func, path, raise_for_status, package=None):
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
        if raise_for_status is True:
            returned.raise_for_status()
    except Exception:
        print(traceback.format_exc())
        raise HTTPError()

    return returned
