import flask
import requests
from flask import make_response, render_template, redirect, url_for

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.forms.create_login import CreateLogin

"""
This file contains the route for user login.
"""


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    The function for rendering a login page when the '/login/' endpoint is called.
    The page contains a form.
    If the form is filled in, it is checked and validated by the CreateLogin form class.
    If it is validated. Information (email, password) is sent to the api to get a session.
    The session is stored into a cookie and then into the session dictionary.
    This is then used to authenticate the user.
    :return: Renders and returns the login page with the flask form.
    """
    session_path = "session/"
    form = CreateLogin()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        dict = {'password': password}
        res = requests.post(app.config['API_PATH'] + session_path + email, data=dict)
        var = res.status_code
        res = res.text
        response = make_response('cookie', 200)
        response.set_cookie('sessionID', str(res), max_age=1000000)

        flask.session['sessionID'] = res
        if var == 200:
            return redirect(url_for("homepage"))
    return render_template('loginpage.html', title="login page", form=form)
