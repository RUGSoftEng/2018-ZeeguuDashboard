from flask import redirect, render_template, request

from app import app
from app.forms.create_cohort import CreateCohort
from app.forms.edit_cohort import EditCohort
from app.util.classroom import load_students, load_class_info, remove_class, create_class, format_class_table_data, \
    edit_class_info, add_student_learning_proportion
from app.util.permissions import has_class_permission, has_session
from app.page_routes.homepage import homepage

"""
This file takes care of all of the class related page_routes:
- loading the class,
- editing it
- removing it
- creating new classes
"""


@app.route('/class/<class_id>/<filter_table_time>/', methods=['GET'])
def class_page_set_cookie(class_id, filter_table_time):
    """
    Sets cookie for filter table time
    :param class_id: the id for this class.
    :param filter_table_time: time for the filter_table
    :return: Renders and returns a class page.
    """
    redirect_to_index = redirect('/class/' + class_id + '/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('filter_table_time', filter_table_time, max_age=60 * 60 * 24 * 365 * 2)
    return response


@app.route('/class/<class_id>/', methods=['GET', 'POST'])
@has_class_permission
def load_class(class_id):
    """
    Function for loading a class of students when the proper route '/class/<class_id>/' is called.
    Requires permission (the logged in user must be a teacher of the class). The class is loaded,
    when the 'GET' method is used. If the 'POST' method is used, the class is deleted.
    :param class_id: The id number of the class.
    :return: Renders and returns a class page.
    """
    if request.method == 'GET':
        filter_table_time = request.cookies.get('filter_table_time')
        if not filter_table_time:
            filter_table_time = time = app.config["DEFAULT_STUDENT_TIME"]

        time = request.cookies.get('time')
        if not time:
            time = app.config["DEFAULT_STUDENT_TIME"]

        students = None
        github_tables = None

        if int(filter_table_time) > int(time):
            students = load_students(class_id, filter_table_time)
            github_tables = format_class_table_data(students, filter_table_time)
            students = load_students(class_id, time)
        else:
            students = load_students(class_id, time)
            github_tables = format_class_table_data(students, filter_table_time)

        if students is None:
            return redirect('/')
        students = add_student_learning_proportion(students)
        class_info = load_class_info(class_id)
        if not students or not github_tables:
            return render_template("empty_classpage.html", class_info=class_info)
        return render_template('classpage.html',
                               title=class_info['name'],
                               students=students,
                               github_tables=github_tables,
                               class_info=class_info,
                               class_id=class_id,
                               time=filter_table_time
                               )



@app.route('/remove_class/<class_id>/', methods=['GET'])
@has_class_permission
def remove(class_id):
    remove_class(class_id)
    messages = ["Sucessfully removed class."]
    return homepage(messages)

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
    form = EditCohort(class_info["inv_code"])

    if form.validate_on_submit():
        inv_code = form.inv_code.data
        name = form.class_name.data
        max_students = form.max_students.data
        edit_class_info(class_id=class_id, name=name, invite_code=inv_code, max_students=max_students)
        messages = []
        messages.append("Edit sucessful")
        return homepage(messages)
    return render_template('edit_class.html',
                           title='Edit classroom',
                           form=form,
                           class_info=class_info,
                           )


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
        messages = ["Sucessfully added class."]
        return homepage(messages)

    return render_template('createcohort.html',
                           title='Create classroom',
                           form=form
                           )
