from flask import Flask

app = Flask(__name__)

from app.page_routes import homepage, errorpages, login, studentpage, classroom
