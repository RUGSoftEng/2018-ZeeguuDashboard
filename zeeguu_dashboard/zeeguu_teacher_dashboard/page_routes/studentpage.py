from flask import render_template, redirect, request

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.util.classroom import load_class_info
from zeeguu_teacher_dashboard.util.permissions import has_student_permission
from zeeguu_teacher_dashboard.util.user import load_user_data, load_user_info, filter_user_bookmarks, get_correct_time, sort_user_bookmarks

"""
This file contains the routes for a student page.
"""


@app.route('/class/<class_id>/student/<student_id>/', methods=['GET'])
@has_student_permission
def student_page(class_id,student_id):
    """
    This loads the student page. When a cookie is set, it's used to set the time filter to show.
    Otherwise, the default_time is used as requested by the customer.
    :param student_id: the student id to use
    :return: the template
    """
    time = request.cookies.get('time')
    if not time or time == "None":
        time = app.config["DEFAULT_STUDENT_TIME"]
    bookmarks = load_user_data(user_id=student_id, time=time)
    info = load_user_info(student_id, time)
    time = get_correct_time(time)
    class_name = load_class_info(class_id)["name"]
    if not info:
        return render_template("empty_student_page.html", info=info, title=info['name'], student_id=student_id, time=time, class_name = class_name, class_id = class_id)
    return render_template("studentpage.html", title=info['name'], info=info, stats=bookmarks, student_id=student_id, time=time, class_name = class_name, class_id = class_id)
