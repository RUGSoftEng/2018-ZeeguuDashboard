from flask import render_template, request

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.util.classroom import get_general_cohort_info
from zeeguu_teacher_dashboard.util.permissions import has_student_permission
from zeeguu_teacher_dashboard.util.user import load_user_data, load_user_info, human_readable_time

"""
This file contains the routes for a student page.
"""


@app.route('/class/<class_id>/student/<student_id>/', methods=['GET'])
@has_student_permission
def student_page(class_id, student_id):
    """
    This loads the student page. When a cookie is set, it's used to set the time filter to show.
    Otherwise, the default_time is used as requested by the customer.
    :param student_id: the student id to use
    :return: the template
    """
    time = request.cookies.get('time')
    if not time or time == "None":
        time = app.config["DEFAULT_STUDENT_TIME"]

    articles_by_date = load_user_data(user_id=student_id, time=time)

    total_articles_count = 0
    for each in articles_by_date:
        total_articles_count += len(each['article_list'])

    info = load_user_info(student_id, time)
    time = human_readable_time(time)
    class_name = get_general_cohort_info(class_id)["name"]

    return render_template("studentpage.html", title=info['name'], info=info, articles_by_date=articles_by_date,
                           student_id=student_id,
                           total_articles_count=total_articles_count,
                           time=time, class_name=class_name, class_id=class_id)
