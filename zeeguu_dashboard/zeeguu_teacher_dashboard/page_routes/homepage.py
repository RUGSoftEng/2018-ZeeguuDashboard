from flask import render_template, redirect, url_for

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.util.classroom import load_classes
from zeeguu_teacher_dashboard.util.permissions import has_session

"""
This file contains the routes for the homepage.
"""


@app.route('/')
def to_homepage():
    """
    This route redirects to the homepage, when only the URL is searched by the browser (for convenience).
    :return: Redirects to '/home' endpoint.
    """
    return redirect(url_for("homepage"))


@app.route('/home/')
@has_session
def homepage(messages=[]):
    """
    This shows a teachers corresponding homepage, as long as a session is validated.
    :return: Renders and returns the home page.
    """
    classes = load_classes()
    return render_template('homepage.html', title="Homepage", classes=classes, messages=messages)
