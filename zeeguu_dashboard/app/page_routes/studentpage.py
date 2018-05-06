from flask import render_template, redirect, make_response, request

from app import app
from app.util.permissions import has_student_permission
from app.util.user import load_user_data, load_user_info, filter_user_bookmarks

# This file contains the route to load the student page.
@app.route('/student/<student_id>/', methods=['GET'])
def student_page(student_id):
    time = request.cookies.get('time')
    if not time:
        time = 14

    bookmarks = load_user_data(user_id=student_id, time=time)
    info = load_user_info(student_id)
    bookmarks = filter_user_bookmarks(bookmarks)

    return render_template("studentpage.html", title=info['name'], info=info, stats=bookmarks, student_id=student_id)

@app.route('/student/<student_id>/<time>/', methods=['GET'])
def student_page_set_cookie(student_id, time):
    redirect_to_index = redirect('/student/' + student_id + '/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('time', time, max_age=60*60*24*365*2)
    return response
