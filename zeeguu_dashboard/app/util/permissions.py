import json
from functools import wraps

from flask import redirect, session

from app.api import api_connection


"""
This file contains all of the functions responsible for validating the user on different page_routes.
"""


def check_session():
    """
    Main function to validate the user.
    :return:
    """
    if not 'sessionID' in session.keys():
        session['sessionID'] = '0'

    permission_check = api_connection.api_get('validate').text

    if permission_check == "OK":
        return True
    return False


def has_session(func):
    """
    General decorator to check if the teacher is logged in.
    :param func:
    :return:
    """
    @wraps(func)
    def session_wrapper(*args, **kwargs):

        if check_session():
            return func(*args, **kwargs)
        else:
            return redirect("login")

    return session_wrapper


def has_class_permission(func):
    """
    Decorator to check if the teacher has access to a page.
    :param func:
    :return:
    """
    @wraps(func)
    def class_permission_wrapper(class_id):
        """

        :param class_id:
        :return:
        """
        if not check_session():
            return redirect('401')
        permission_check = api_connection.api_get('has_permission_for_cohort/' + str(class_id)).text
        if permission_check == "OK":
            return func(class_id)
        else:
            return redirect('401')

    return class_permission_wrapper


def has_student_permission(func):
    """
    This function checks if an authenticated user has permission to check a student page.
    :param func:
    :return:
    """

    @wraps(func)
    def student_permission_wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if not check_session():
            return redirect('401')

        """
        permission_check and time are possible arguments of func
        permission_check is initialized to an empty string and
        time is initialized to the standard time frame for bookmarks
        """
        permission_check = ''
        time = 14

        for key, value in kwargs.iteritems():
            if key == "student_id":
                permission_check = api_connection.api_get('has_permission_for_user_info/' + str(value)).text

            if key == "time":
                time = int(value)

        if permission_check == "OK" and int(time) < 366:
            return func(*args, **kwargs)
        else:
            return redirect('401')

    return student_permission_wrapper
