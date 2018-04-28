from functools import wraps

from flask import redirect, session
import app as application
import app.util
import json

def check_session():
    if not 'sessionID' in session.keys():
        session['sessionID'] = '0'

    permission_check = app.util.api_get('validate').text

    if permission_check == "OK":
        return True
    return False

#General decorator to check if the teacher is logged in
def has_session(func):

    @wraps(func)
    def session_wrapper(*args, **kwargs):

        if check_session():
           return func(*args, **kwargs)
        else:
          return redirect("login")

    return session_wrapper


#Decorator to check if the teacher has access to a page. CURRENTLY ONLY WORKS FOR CLASS PERMISSIONS
def has_class_permission(func):

    @wraps(func)
    def class_permission_wrapper(class_id):
        if not check_session():
            return redirect('401')
        permission_check = app.util.api_get('has_permission_for_cohort/' + str(class_id)).text
        if permission_check == "OK":
            return func(class_id)
        else:
            return redirect('401')

    return class_permission_wrapper

def has_student_permission(func):

    @wraps(func)
    def student_permission_wrapper(user_id):
        if not check_session():
            return redirect('401')
        permission_check = app.util.api_get('has_permission_for_user_info/' + str(user_id)).text
        if permission_check == "OK":
            return func(user_id)
        else:
            return redirect('401')

    return student_permission_wrapper