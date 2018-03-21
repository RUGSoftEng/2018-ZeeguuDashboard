from flask import render_template, flash, redirect, session
from app import app
from app.createcohort import CreateCohort
from app.loginform import CreateLogin
import requests
import json
path = "http://51.15.89.64:9001/"


@app.route('/')
def homepage():
    return redirect("/teacher_id/1")

@app.route('/teacher_id/<teacher_id>/')
def template(teacher_id):
    #This loads in the JavaScript object notation of the class id's
    returned_class_ids_string = requests.get(path + "get_classes_by_teacher_id/"+str(teacher_id)).text
    #This convers the notation to an int list
    returned_class_ids = json.loads(returned_class_ids_string)
    classes = []
    #For each int in the int list, this will return class_name and add it to classes.
    for id in returned_class_ids:
        #This loads in json for info(Dictionary) of class with id class_Id
        class_info_string = requests.get(path+'get_class_info/' + str(id)).text
        #This convers json to dictionary
        class_info = json.loads(class_info_string)
        new_class = {
            #This gets 'class_name' from class_info dictionary
            'class':class_info['class_name'],
            'id':class_info['class_id'],
            'teacher_id':teacher_id,
        }
        classes.append(new_class)

    return render_template('homepage.html', title="Homepage", classes=classes)


#I updated this function to show some functionality to loading data from api.
#Try add a new class, it works! (if class_id exists. And if teacher_id exists)
@app.route('/class/<teacher_id>/<class_id>')
def load_class(teacher_id, class_id):
    #this returns all the students of a class
    print("class id is " + str(class_id))
    returned_student_ids_string = requests.get(path + "get_users_from_class/"+str(class_id)).text
    print(returned_student_ids_string)
    returned_student_ids = json.loads(returned_student_ids_string)
    students = []
    for id in returned_student_ids:
        student_name = requests.get(path + 'get_user_name/' + str(id)).text
        print("Adding student " + student_name)
        new_student = {
            'student': student_name,
            'reading': 20,
            'exercises': 30,
            'article': 'place holder'
        }
        students.append(new_student)

    return render_template('classpage.html', title=str(class_id), students=students)


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
        response = requests.post(path+ "add_class", data=package)
        return redirect('/')
    return render_template('createcohort.html', title = 'Create classroom', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = CreateLogin()
    print("gets here")
    if form.validate_on_submit():
        print("also gets here")
        email = form.email.data
        password = form.password.data
        dict = {'password':password}
        response = requests.post(path+"session/"+email, data =dict)
        session['session'] = response.text
        print(response.text)
    return render_template('loginpage.html', title = "login page",form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e)