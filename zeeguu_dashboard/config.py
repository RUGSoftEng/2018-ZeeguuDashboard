import os

class Config(object):
    """

    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_PATH = os.environ.get('API_PATH')

    