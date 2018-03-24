import functools

from flask import redirect, session
import app as application
import app.util
import json

def check_session():
    my_boolean = app.util.api_get('has_session').text
    my_boolean = json.loads(my_boolean)
    if my_boolean == 1:
        return True
    return False

#General decorator to check if the teacher is logged in
def has_session(func):

    @functools.wraps(func)
    def session_wrapper(*args, **kwargs):

        if check_session():
           return func(*args, **kwargs)
        else:
          return redirect("login")

    return session_wrapper


#Decorator to check if the teacher has access to a page. CURRENTLY ONLY WORKS FOR CLASS PERMISSIONS
def has_permission(func):


    @functools.wraps(func)
    def permission_wrapper(class_id):
        if not check_session():
            return redirect('401')
        my_boolean = app.util.api_get('get_class_permissions/' + str(class_id)).text
        my_boolean = json.loads(my_boolean)
        print(my_boolean)
        if my_boolean == 1:
            return func(class_id)
        else:
            return redirect('401')

    return permission_wrapper