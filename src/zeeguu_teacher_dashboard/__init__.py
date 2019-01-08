from flask import Flask

app = Flask(__name__)

# These imports have be issued after the app is initialized due to how Flask works.
from .page_routes import homepage, errorpages, login, studentpage, classroom
