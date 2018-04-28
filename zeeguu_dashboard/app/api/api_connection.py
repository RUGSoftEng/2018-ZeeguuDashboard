import flask
import requests

from app import app


def api_post(path, package):
    _api_call('post', path=path, package=package)


def api_get(path):
    return _api_call('get', path=path)


def _api_call(function, path, package=None):
    params = {
        'session': flask.session['sessionID']
    }
    returned = None
    try:
        if function is 'get':
            returned = requests.get(app.config['API_PATH'] + path, params=params)
        else:
            requests.post(app.config['API_PATH'] + path, data=package, params=params)
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise Exception("Exception while performing request.")
    return returned
