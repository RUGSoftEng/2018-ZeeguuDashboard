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
    This function is executed when the '/student/<student_id>/<time>/' endpoint is called.
    It is used for rendering a student page for a specific student and time frame.
    It loads the bookmarks from the Zeeguu_API as well as the user information.
    It then filters out unnecessary bookmarks (see the filter_user_bookmarks function for more detail).
    :param student_id: The id number of the student.
    :param time: The time frame for the bookmarks (how many days of bookmarks do you want to see).
    :return: Renders and returns the student page.
    """
    bookmarks = load_user_data(user_id=student_id, time=time)
    info = load_user_info(student_id)
    bookmarks = filter_user_bookmarks(bookmarks)
    return render_template("studentpage.html", title=info['name'], info=info, stats=bookmarks, student_id=student_id)
