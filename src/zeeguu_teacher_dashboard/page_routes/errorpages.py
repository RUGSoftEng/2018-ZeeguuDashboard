from flask import render_template
from requests import HTTPError

from zeeguu_teacher_dashboard import app

"""
This file contains all of the error page routes.
"""


@app.errorhandler(HTTPError)
def page_not_found(HTTPError):
    """
    Function for handling a raised status exception from a status code in the api call. The expection in question
    is a requests.HTTPError. This exception usually happens when there is a problem with calling the Zeeguu API.
    :return: Renders and returns an error page.
    """
    errorString = "There seems to be a problem with the Zeeguu server, please try again later or contact the Zeeguu team."
    return render_template("errorpage.html", exception=errorString)


@app.errorhandler(400)
@app.route("/400")
def invalid_request():
    """
    Function for loading the 401 error page when page when logged in user and unautherised.
    :return: Renders and returns an error page.
    """
    return render_template("errorpage.html", exception="400: Invalid request")


@app.errorhandler(401)
@app.route("/401")
def invalid_credentials():
    """
    Function for loading the 401 error page when page when logged in user and unautherised.
    :return: Renders and returns an error page.
    """
    return render_template("errorpage.html", exception="401 Unauthorized: You do not have access to this page.")


@app.errorhandler(404)
def page_not_found(e):
    """
    Function for loading the 404 error page when requested url does not exist.
    :return: Renders and returns an error page.
    """
    return render_template("errorpage.html", exception="404 Not Found: The requested URL was not found on the server.")
