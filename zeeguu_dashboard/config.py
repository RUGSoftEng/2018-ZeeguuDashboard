import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    if os.environ['DASHBOARD_API'] == 'local':
        API_PATH = "localhost:9001"
    else:
        API_PATH = "http://51.15.89.64:9001/"
