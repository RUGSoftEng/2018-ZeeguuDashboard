import flask
from flask import render_template, flash, redirect, session, Flask, make_response
from app import app
from app.createcohort import CreateCohort
from app.loginform import CreateLogin
from app.util import load_students, load_classes, api_get, api_post, load_user_data, filter_user_bookmarks
from app.permissions import has_session, has_class_permission, has_student_permission
import requests
import json
path = "http://51.15.89.64:9001/"
#path = "http://0.0.0.0:9001/"

@app.route('/')
def homepage():
    return redirect("teacher")

@app.route('/teacher')
@has_session
def template():
    classes = load_classes()
    return render_template('homepage.html', title="Homepage", classes=classes)


#I updated this function to show some functionality to loading data from api.
#Try add a new class, it works! (if class_id exists. And if teacher_id exists)
@app.route('/class/<class_id>')
@has_class_permission
def load_class(class_id):
    students = load_students(class_id)
    if(students is None):
        return redirect('/')
    return render_template('classpage.html', title='DashBoard', students=students)

## FRONT END TEAM -- USE
@app.route('/class/student/<user_id>')
@has_student_permission
def load_user(user_id):
    stats = load_user_data(user_id = user_id)
    ## implement HTML here
    return render_template("studentpage.html", title = "activity", stats = stats)


# This works if class_inv is not taken and teacher_id exists.
@app.route('/create_classroom',  methods=['GET', 'POST'])
@has_session
def create_classroom():
    form = CreateCohort()
    if form.validate_on_submit():
        class_name = form.class_name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        class_language_id = form.class_language_id.data
        package = {'class_name': class_name, 'inv_code': inv_code, 'max_students': max_students,
                  'class_language_id': class_language_id}
        api_post('add_class',package)
        return redirect('/')
    return render_template('createcohort.html', title = 'Create classroom', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = CreateLogin()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        dict = {'password':password}
        res = requests.post(path+"session/"+email, data =dict).text


        # As far a i can tell this does nothing but will be useful later!
        response = make_response('cookie',200)
        response.set_cookie('sessionID', str(res), max_age=1000000)
        #############################################

        #This actually sets the session that is used.
        flask.session['sessionID'] = res

    return render_template('loginpage.html', title = "login page",form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e)

@app.errorhandler(401)
def invalid_credentials(e):
    return render_template("404.html", e=e)


