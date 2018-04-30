import sys
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app.page_routes import homepage, errorpages, login, studentpage, classroom

arguments = sys.argv
if len(arguments) > 0:
    for arg in arguments:
        if arg == 'Debug':
            app.debug = True

app.run()