from flask import render_template, flash, redirect
from app import app
from app.createcohort import CreateCohort
import requests
import jsonify

@app.route('/')
def template():
	classes = [
        {
            'class': 'chinese',
            'id': '1'
        },
        {
            'class': 'dutch',
            'id': '2'
        },
        {
            'class': 'german',
            'id': '3'
         }
	]
	return render_template('homepage.html', title='Zeeguu2.0', classes=classes)

@app.route('/class/<idx>')
def spanish(idx):
    students = ['John','Mary']
    idx = int(idx)
    return render_template('classpage.html', title = 'Spanish class', relevant=students[idx], range=range(10))

@app.route('/create_classroom',  methods=['GET', 'POST'])
def create_classroom():
    form = CreateCohort()
    if form.validate_on_submit():
        #return requests.get("http://0.0.0.0:9001/get_user_name/1").text
        class_name = form.class_name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        teacher_id = form.teacher_id.data
        class_language_id = form.class_language_id.data
        package = {'class_name':class_name, 'inv_code':inv_code, 'max_students':max_students, 'teacher_id':teacher_id, 'class_language_id':class_language_id}
        response = requests.post("http://0.0.0.0:9001/add_class", data = package)
        print(response)

    return render_template('createcohort.html', title = 'Create classroom', form=form)

