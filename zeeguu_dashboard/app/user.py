from flask import render_template

from app import app
from app.util.permissions import has_student_permission
from app.util.user import load_user_data, load_user_info


@app.route('/student/<user_id>/')
@has_student_permission
def load_user(user_id):
    stats = load_user_data(user_id=user_id)
    info = load_user_info(user_id)
    return render_template("studentpage.html", title=info['name'], info=info, stats=stats)
