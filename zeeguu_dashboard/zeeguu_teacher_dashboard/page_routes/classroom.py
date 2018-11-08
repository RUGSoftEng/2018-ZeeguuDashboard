from flask import redirect, render_template, request

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.forms.create_cohort import CreateCohort
from zeeguu_teacher_dashboard.forms.edit_cohort import EditCohort
from zeeguu_teacher_dashboard.util.classroom import load_students, get_general_cohort_info, remove_class, create_class, \
    format_class_table_data, \
    update_class_info, add_student_learning_proportion, add_total_and_normalized_time
from zeeguu_teacher_dashboard.util.permissions import has_class_permission, has_session
from zeeguu_teacher_dashboard.page_routes.homepage import homepage
from zeeguu_teacher_dashboard.util.user import human_readable_time

"""
This file takes care of all of the class related page_routes:
- loading the class,
- editing it
- removing it
- creating new classes
"""


@app.route('/class/<class_id>/', methods=['GET', 'POST'])
@has_class_permission
def load_class(class_id, messages=[]):
    """
    Function for loading a class of students when the proper route '/class/<class_id>/' is called.
    Requires permission (the logged in user must be a teacher of the class). The class is loaded,
    when the 'GET' method is used. If the 'POST' method is used, the class is deleted.
    :param class_id: The id number of the class.
    :return: Renders and returns a class page.
    """

    time = request.cookies.get('time')
    if not time:
        time = app.config["DEFAULT_STUDENT_TIME"]

    students = load_students(class_id, time)

    if students is None:
        return redirect('/')

    add_student_learning_proportion(students)
    add_total_and_normalized_time(students)

    general_cohort_info = get_general_cohort_info(class_id)

    if not students:
        return render_template("empty_classpage.html", class_info=general_cohort_info, class_id=class_id)

    students = sorted(students, key=lambda x: x['total_time'], reverse=True)

    return render_template('classpage.html',
                           title=general_cohort_info['name'],
                           students=students,
                           class_info=general_cohort_info,
                           class_id=class_id,
                           display_time_interval=human_readable_time(time),
                           messages=messages
                           )


@app.route('/remove_class/<class_id>/', methods=['GET'])
@has_class_permission
def remove_class_route(class_id):
    print("class_id!!!" + str(class_id))
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
    class_info = get_general_cohort_info(class_id)

    form = EditCohort(class_info["inv_code"], request.form, **class_info)

    if request.method == 'POST' and form.validate():
        inv_code = form.inv_code.data
        name = form.name.data

        update_class_info(class_id=class_id,
                          name=name,
                          invite_code=inv_code,
                          declared_level_min=form.declared_level_min.data,
                          declared_level_max=form.declared_level_max.data)
        messages = []
        messages.append("Edit sucessful")
        return load_class(class_id, messages)

    print("class_id!!!" + str(class_id))
    return render_template('edit_class.html',
                           title='Edit classroom',
                           form=form,
                           class_info=class_info,
                           class_id=class_id
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
        name = form.name.data
        inv_code = form.inv_code.data
        max_students = form.max_students.data
        language_id = form.class_language_id.data
        create_class(name=name, inv_code=inv_code, max_students=max_students, language_id=language_id)
        messages = ["Sucessfully added class."]
        return homepage(messages)

    return render_template('create_class.html',
                           title='Create classroom',
                           form=form
                           )
