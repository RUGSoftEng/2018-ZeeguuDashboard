from flask import render_template
from app import app


"""
This file contains all of the error page routes.
"""
@app.errorhandler(401)
@app.route("/401")
def invalid_credentials():
    print("called 401")
    """
    :param e:
    :return:
    """
    return render_template("errorpage.html", exception="401 UNAUTHORIZED")


@app.errorhandler(404)
def page_not_found(e):
    print("called 404")
    """
    :param e:
    :return:
    """
    return render_template("errorpage.html", exception="404 Not Found: The requested URL was not found on the server.")


