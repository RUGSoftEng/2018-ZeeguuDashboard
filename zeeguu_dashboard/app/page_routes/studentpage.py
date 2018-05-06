from flask import render_template, redirect, make_response

from app import app
from app.util.permissions import has_student_permission
from app.util.user import load_user_data, load_user_info, filter_user_bookmarks


"""
This file contains the route to load the student page.
"""
@app.route('/student/<student_id>/<time>/', methods=['GET'])
@has_student_permission
def student_page(student_id, time):
    """

    :param student_id:
    :param time:
    :return:
    """
    bookmarks = load_user_data(user_id=student_id, time=time)
    info = load_user_info(student_id)
    bookmarks = filter_user_bookmarks(bookmarks)
    return render_template("studentpage.html", title=info['name'], info=info, stats=bookmarks, student_id=student_id)
