from flask import render_template, redirect, make_response, request

from app import app
from app.util.permissions import has_student_permission
from app.util.user import load_user_data, load_user_info, filter_user_bookmarks

"""
This file contains the routes for a student page.
"""


@app.route('/student/<student_id>/', methods=['GET'])
@has_student_permission
def student_page(student_id):
    """
    This loads the student page. When a cookie is set, it's used to set the time filter to show.
    Otherwise, the default_time is used, which is 14, as requested by the customer.
    :param student_id: the student id to use
    :return: the template
    """
    DEFAULT_TIME = 14
    time = request.cookies.get('time')
    if not time:
        time = DEFAULT_TIME
    bookmarks = load_user_data(user_id=student_id, time=time)
    info = load_user_info(student_id)
    bookmarks = filter_user_bookmarks(bookmarks)
    return render_template("studentpage.html", title=info['name'], info=info, stats=bookmarks, student_id=student_id)


@app.route('/student/<student_id>/<time>/', methods=['GET'])
@has_student_permission
def student_page_set_cookie(student_id, time):
    """
    Loads a student page according to the time given and sets a cookie to it.
    :param student_id: the student id to use
    :param time: the time to filter
    :return: the template
    """
    redirect_to_index = redirect('/student/' + student_id + '/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('time', time, max_age=60 * 60 * 24 * 365 * 2)
    return response
