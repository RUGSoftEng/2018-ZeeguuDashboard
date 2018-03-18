from flask import render_template, flash, redirect
from app import app
from app.createcohort import CreateCohort

@app.route('/')
def template():
    classes = [
        {
            'class': 'Spanish A1',
        },
        {
            'class': 'Spanish B2',
        },
        {
            'class': 'Spanish C1',
        }
    ]
    students = [
        {
            'student': 'Evi',
            'reading': 20,
            'exercises': 30,
            'article': 'skheukf'
        },

        {
            'student': 'Jakob',
            'reading': 30,
            'exercises': 5,
            'exercise': 'fwgeuiftuwek'
        },
        {
            'student': 'Ai',
            'reading': 1,
            'exercises': 55,
            'exercise': 'haahahha'
        }
    ]
    return render_template('classpage.html', title=classes[0].get('class'), classes=classes, students=students)


@app.route('/class/<idx>')
def spanish(idx):
    students = [
        {
            'student': {'username': 'Evi'},
            'reading': 20,
            'exercises': 30,
            'last today': {'article': 'skheukf'}
        },

        {
            'student': {'username': 'Jakob'},
            'reading': 30,
            'exercises': 50,
            'last today': {'exercise': 'fwgeuiftuwek'}
        },
        {
            'student': {'username': 'Ai'},
            'reading': 1,
            'exercises': 2,
            'last today': {'exercise': 'haahahha'}
        }
    ]
    idx = int(idx)
    return render_template('classpage.html', title = 'Spanish class', relevant=students[idx], range=range(3))


@app.route('/create_classroom',  methods=['GET', 'POST'])
def create_classroom():
    form = CreateCohort()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('createcohort.html', title = 'Create classroom', form=form)