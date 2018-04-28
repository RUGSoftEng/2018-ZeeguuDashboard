from flask import render_template
from app import app


# This file contains all of the error page routes.


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", exception=e)


@app.errorhandler(401)
def invalid_credentials(e):
    return render_template("404.html", exception=e)
