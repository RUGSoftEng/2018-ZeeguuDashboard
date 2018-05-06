from flask import render_template
from app import app


"""
This file contains all of the error page routes.
"""


@app.errorhandler(404)
def page_not_found(e):
    """

    :param e:
    :return:
    """
    return render_template("errorpage.html", exception=e)


@app.errorhandler(401)
def invalid_credentials(e):
    """

    :param e:
    :return:
    """
    return render_template("errorpage.html", exception=e)
