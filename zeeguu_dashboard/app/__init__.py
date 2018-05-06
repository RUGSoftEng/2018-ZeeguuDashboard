import sys

from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app.page_routes import homepage, errorpages, login, studentpage, classroom

arguments = sys.argv
if len(arguments) > 0:
    for arg in arguments:
        if arg == 'Debug':
            app.debug = True
