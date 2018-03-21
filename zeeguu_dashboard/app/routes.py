import flask
from flask import render_template, flash, redirect, session, Flask, make_response
from app import app
from app.createcohort import CreateCohort
from app.loginform import CreateLogin
import requests
import json
path = "http://51.15.89.64:9001/"

@app.route('/')
def homepage():
    return redirect("teacher")

@app.route('/teacher')
def template():
    classes = load_classes()
    return render_template('homepage.html', title="Homepage", classes=classes)


#I updated this function to show some functionality to loading data from api.
#Try add a new class, it works! (if class_id exists. And if teacher_id exists)
@app.route('/class/<class_id>')
def load_class(class_id):
    students = load_students(class_id)
    return render_template('classpage.html', title='DashBoard!', students=students)


# This works if class_inv is not taken and teacher_id exists.
@app.route('/create_classroom',  methods=['GET', 'POST'])
def create_classroom():
    form = CreateCohort()
    if form.validate_on_submit():
        class_name = form.class_name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        teacher_id = form.teacher_id.data
        class_language_id = form.class_language_id.data
        package = {'class_name': class_name, 'inv_code': inv_code, 'max_students': max_students,
                   'teacher_id': teacher_id, 'class_language_id': class_language_id}
        api_post('add_class',package)
        return redirect('/')
    return render_template('createcohort.html', title = 'Create classroom', form=form)

@app.route('/login', methods=['GET', 'POST'])
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



def load_classes():
    # This loads in the JavaScript object notation of the class id's
    returned_class_ids_string = api_get("get_classes").text
    # This convers the notation to an int list
    returned_class_ids = json.loads(returned_class_ids_string)
    classes = []
    # For each int in the int list, this will return class_name and add it to classes.
    for id in returned_class_ids:
        # This loads in json for info(Dictionary) of class with id class_Id
        class_info_string = api_get('get_class_info/' + str(id)).text
        # This convers json to dictionary
        class_info = json.loads(class_info_string)
        new_class = {
            # This gets 'class_name' from class_info dictionary
            'class': class_info['class_name'],
            'id': class_info['class_id'],
            'teacher_id': 1 #this needs to be coded in if you need teacher_id
        }
        classes.append(new_class)
    return classes


def load_students(class_id):
    # this returns all the students of a class
    print("class id is " + str(class_id))
    returned_student_ids_string = api_get("get_users_from_class/" + str(class_id)).text
    # returned_student_ids_string = requests.get(path + "get_users_from_class/"+str(class_id)).text
    print(returned_student_ids_string)
    returned_student_ids = json.loads(returned_student_ids_string)
    students = []
    for id in returned_student_ids:

        user_info = json.loads(api_get('get_user_info/'+str(id)).text)
        print("Adding student " + user_info['name'])
        new_student = {
            'student': user_info['name'],
            'reading': user_info['reading_time'],
            'exercises': user_info['exercises_done'],
            'article': user_info['last_article']
        }
        students.append(new_student)
    return students

def api_post(function, package):
    params = {
        'session':flask.session['sessionID']
    }
    requests.post(path+function, data=package, params=params)


def api_get(function):
    params = {
        'session': flask.session['sessionID']
    }
    returned = requests.get(path+function, params = params)
    return returned