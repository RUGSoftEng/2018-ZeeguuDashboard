import json
from functools import wraps

from flask import redirect, session

<<<<<<< HEAD:zeeguu_dashboard/app/util/permissions.py
from app.api import api_connection
=======
import app.api.api_connection
>>>>>>> d3e15721a03228a1a969f42c1fcb8d2d44f2e2a6:zeeguu_dashboard/app/util/permissions.py


def check_session():
    if not 'sessionID' in session.keys():
        session['sessionID'] = '0'

<<<<<<< HEAD:zeeguu_dashboard/app/util/permissions.py
    permission_check = api_connection.api_get('validate').text

    if permission_check == "OK":
=======
    permission_bool = app.api.api_connection.api_get('has_session').text
    permission_bool = json.loads(permission_bool)
    if permission_bool == 1:
>>>>>>> d3e15721a03228a1a969f42c1fcb8d2d44f2e2a6:zeeguu_dashboard/app/util/permissions.py
        return True
    return False


# General decorator to check if the teacher is logged in
def has_session(func):
    @wraps(func)
    def session_wrapper(*args, **kwargs):

        if check_session():
            return func(*args, **kwargs)
        else:
            return redirect("login")

    return session_wrapper


# Decorator to check if the teacher has access to a page.
def has_class_permission(func):
    @wraps(func)
    def class_permission_wrapper(class_id):
        if not check_session():
            return redirect('401')
<<<<<<< HEAD:zeeguu_dashboard/app/util/permissions.py
        permission_check = api_connection.api_get('has_permission_for_cohort/' + str(class_id)).text
        if permission_check == "OK":
=======
        permission_bool = app.api.api_connection.api_get('test_cohort_permissions/' + str(class_id)).text
        permission_bool = json.loads(permission_bool)
        if permission_bool == 1:
>>>>>>> d3e15721a03228a1a969f42c1fcb8d2d44f2e2a6:zeeguu_dashboard/app/util/permissions.py
            return func(class_id)
        else:
            return redirect('401')

    return class_permission_wrapper


def has_student_permission(func):
    @wraps(func)
    def student_permission_wrapper(user_id):
        if not check_session():
            return redirect('401')
<<<<<<< HEAD:zeeguu_dashboard/app/util/permissions.py
        permission_check = api_connection.api_get('has_permission_for_user_info/' + str(user_id)).text
        if permission_check == "OK":
=======
        permission_bool = app.api.api_connection.api_get('test_user_permissions/' + str(user_id)).text
        permission_bool = json.loads(permission_bool)
        if permission_bool == 1:
>>>>>>> d3e15721a03228a1a969f42c1fcb8d2d44f2e2a6:zeeguu_dashboard/app/util/permissions.py
            return func(user_id)
        else:
            return redirect('401')

    return student_permission_wrapper
