import flask
import requests
from flask import render_template, redirect, make_response

from app import app
from app.util.classroom import load_classes
from app.util.forms import CreateLogin
from app.util.permissions import has_session

session_path = "session/"


@app.route('/')
def homepage():
    return redirect("/teacher")


@app.route('/teacher/')
@has_session
def template():
    classes = load_classes()
    return render_template('homepage.html', title="Homepage", classes=classes)


@app.route('/login/', methods=['GET', 'POST'])
def login():
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
