from flask import redirect, render_template

from app import app
from app.api.api_connection import api_post
from app.util.classroom import load_students, load_class_info, remove_class, create_class
from app.util.forms import EditCohort, CreateCohort
from app.util.permissions import has_class_permission, has_session

"""
This file takes care of all of the class related page_routes:
- loading the class,
- editing it
- removing it
- creating new classes
"""


@app.route('/class/<class_id>/')
@has_class_permission
def load_class(class_id):
    """

    :param class_id:
    :return:
    """
    students = load_students(class_id)
    if students is None:
        return redirect('/')
    class_info = load_class_info(class_id)
    return render_template('classpage.html', title=class_info['name'], students=students, class_info=class_info)


@app.route('/edit_class/<class_id>/', methods=['GET', 'POST'])
@has_class_permission
def edit_class(class_id):
    """

    :param class_id:
    :return:
    """
    class_info = load_class_info(class_id)
    form = EditCohort()
    if form.validate_on_submit():
        inv_code = form.inv_code.data
        name = form.class_name.data
        max_students = form.max_students.data
        package = {'name': name, 'inv_code': inv_code, 'max_students': max_students}
        api_post('update_cohort/' + str(class_id), package)
        return redirect('/')
    return render_template('edit_class.html', title='Edit classroom', form=form, class_info=class_info)


@app.route('/remove_class/<class_id>/')
@has_class_permission
def remove_classroom(class_id):
    """

    :param class_id:
    :return:
    """
    remove_class(class_id)
    return redirect('/')


@app.route('/create_classroom/', methods=['GET', 'POST'])
@has_session
def create_classroom():
    """

    :return:
    """
    form = CreateCohort()
    if form.validate_on_submit():
        name = form.class_name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        language_id = form.class_language_id.data
        create_class(name=name, inv_code=inv_code, max_students=max_students, language_id=language_id)
        return redirect('/')

    return render_template('createcohort.html', title='Create classroom', form=form)
