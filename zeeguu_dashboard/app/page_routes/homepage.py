from flask import render_template, redirect

from app import app
from app.util.classroom import load_classes
from app.util.permissions import has_session


"""
This file contains the routes for the homepage.
"""


@app.route('/')
def to_homepage():
    """
    This route redirects to the homepage, when only the URL is searched by the browser (for convenience).
    :return: Redirects to '/teacher' endpoint.
    """
    return redirect("/teacher")


@app.route('/teacher/')
@has_session
def homepage():
    """
    This shows a teachers corresponding homepage, as long as a session is validated.
    :return:
    """
    classes = load_classes()
    return render_template('homepage.html', title="Homepage", classes=classes)
