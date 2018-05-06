import flask
import requests
from flask import make_response, render_template

from app import app
from app.util.forms import CreateLogin


"""
This file contains the route for user login.
"""


session_path = "session/"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """

    :return:
    """
    form = CreateLogin()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        dict = {'password': password}
        res = requests.post(app.config['API_PATH'] + session_path + email, data=dict).text

        response = make_response('cookie', 200)
        response.set_cookie('sessionID', str(res), max_age=1000000)

        flask.session['sessionID'] = res

    return render_template('loginpage.html', title="login page", form=form)
