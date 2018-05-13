from flask import redirect, render_template, request

from app import app
from app.api import api_connection
from app.forms.create_cohort import CreateCohort
from app.forms.edit_cohort import EditCohort
from app.util.classroom import load_students, load_class_info, remove_class, create_class, format_class_table_data
from app.util.permissions import has_class_permission, has_session
from app.util.classroom import reformat_time_spent

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
    Function for loading a class of students when the proper route '/class/<class_id>/' is called.
    Requires permission (the logged in user must be a teacher of the class).
    :param class_id: The id number of the class.
    :return: Renders and returns a class page.
    """
    students = load_students(class_id)
    if students is None:
        return redirect('/')
    class_info = load_class_info(class_id)
    time = request.cookies.get('time')
    if not time:
        time = 14

    students = reformat_time_spent(students)

    return render_template('classpage.html',
                           title=class_info['name'],
                           students=students,
                           class_info=class_info,
                           time=str(time)
                           )


@app.route('/edit_class/<class_id>/', methods=['GET', 'POST'])
@has_class_permission
def edit_class(class_id):
    """
    Function for loading an edit class page when the proper route '/edit_class/<class_id>' is called.
    Requires permission (the logged in user must be a teacher of the class).
    :param class_id: The id number of the class.
    :return: Renders and returns an edit class page.
    """
    class_info = load_class_info(class_id)
    form = EditCohort()
    if form.validate_on_submit():
        inv_code = form.inv_code.data
        name = form.class_name.data
        max_students = form.max_students.data
        package = {'name': name, 'inv_code': inv_code, 'max_students': max_students}
        api_connection.api_get('update_cohort/' + str(class_id), package)
        return redirect('/')
    return render_template('edit_class.html',
                           title='Edit classroom',
                           form=form,
                           class_info=class_info
                           )


@app.route('/remove_class/<class_id>/')
@has_class_permission
def remove_classroom(class_id):
    """
    Function for removing a class when the proper route '/remove_class/<class_id>' is called.
    Removes the class and redirects the user to the home page.
    Requires permission (the logged in user must be a teacher of the class).
    :param class_id: The id number of the class.
    :return: Redirects the user to the home page.
    """
    remove_class(class_id)
    return redirect('/')


@app.route('/create_classroom/', methods=['GET', 'POST'])
@has_session
def create_classroom():
    """
    Function for loading a create class page when the proper route '/create_classroom/' is called.
    Requires a session (the user must be logged in).
    :return: Renders and returns a create class page.
    """
    form = CreateCohort()
    if form.validate_on_submit():
        name = form.class_name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        language_id = form.class_language_id.data
        create_class(name=name, inv_code=inv_code, max_students=max_students, language_id=language_id)
        return redirect('/')

    return render_template('createcohort.html',
                           title='Create classroom',
                           form=form
                           )
