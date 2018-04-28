from flask import render_template

from app import app
from app.util.permissions import has_student_permission
from app.util.user import load_user_data, load_user_info


# This file contains the route to load the student page.


@app.route('/student/<student_id>/', methods=['GET'])
@has_student_permission
def student_page(student_id):
    stats = load_user_data(user_id=student_id)
    info = load_user_info(student_id)
    return render_template("studentpage.html", title=info['name'], info=info, stats=stats)
