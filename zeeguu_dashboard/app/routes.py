from flask import render_template, flash, redirect
from app import app
from app.createcohort import CreateCohort

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
        return redirect('/')
    return render_template('createcohort.html', title = 'Create classroom', form=form)

