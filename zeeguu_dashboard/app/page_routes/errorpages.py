from flask import render_template
from app import app


"""
This file contains all of the error page routes.
"""


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


