import json

from app.api.api_connection import api_post, api_get

"""
This file contains all of the utility functions required to get and format the data for the classroom page,
as well as posting data and changing it.
"""


def create_class(name, inv_code, max_students, language_id):
    """
    Function for creating class.
    Requires permission (the logged in user must be a teacher).
    :param name:
    :param inv_code:
    :param max_students:
    :param language_id:
    :return: return value from the POST request (we expect 'OK')
    """
    package = {'name': name, 'inv_code': inv_code, 'max_students': max_students,
               'language_id': language_id}
    api_post('create_own_cohort', package)


def remove_class(class_id):
    """
    Function for removing class.
    Requires permission (the logged in user must be owner of the class)
    Requires that class is empty.
    :param class_id:
    :return: return value from the POST request (we expect 'OK')
    """
    api_post('remove_cohort/' + str(class_id))


def load_class_info(class_id):
    """
    Function for loading class information. Loads information in JSON format and converts it to dictionary.
    Requires permission (the logged in user must have permission to class)
    :param class_id:
    :return: Dictionary of class information (id, name, language_id, cur_students, max_students)
    """

    returned_class_infos_string = api_get("cohort_info/" + str(class_id))
    returned_class_info = json.loads(returned_class_infos_string)
    class_info = returned_class_info
    return class_info

def edit_class_info(class_id, name, invite_code, max_students):
    """
    Function for editing class information. Makes an API call with the proper data.
    :param class_id: The id number of the class.
    :param name: The name of the class.
    :param invite_code: The invite code of the class for students to join.
    :param max_students: The maximum number of student
    :return:
    """
    package = {'name': name, 'inv_code': invite_code, 'max_students': max_students}
    api_post('update_cohort/' + str(class_id), package=package)

def load_classes():
    """
    Function for loading information on all classes teacher has permission for. Loads information in JSON format and converts it to a dictionary.
    Requires valid session.
    :return: Dictionary of dictionaries of class information (id, name, language_id, cur_students, max_students)
    """
    returned_class_infos_string = api_get("cohorts_info").text
    returned_class_infos = json.loads(returned_class_infos_string)
    classes = returned_class_infos
    return classes


def load_students(class_id):
    """
    Function for loading information on all students in a class. Loads information in JSON format and converts it to a dictionary.
    Requires permission  ( the logged in user must have permission to view class that student is in)
    :param class_id:
    :return: Dictionary of dictionaries containing (id, name, email, reading time, exercises done, last article)
    """
    returned_student_infos_string = api_get("users_from_cohort/" + str(class_id)).text
    returned_student_infos = json.loads(returned_student_infos_string)
    students = returned_student_infos
    return students


def verify_invite_code_exists(inv_code):
    """
    Function for checking if an invite code exists.
    Requires a valid session.
    :param inv_code: this is the code to be checked.
    :return: True or False depending on if the invite code exists in the database.
    """
    inv_code_bool = api_get('invite_code_usable/' + str(inv_code)).text
    if inv_code_bool == "OK":
        return False
    return True

def reformat_time_spent(students):
    """
    This function is a quick hotfix to reformat the user data for jinja2.
    :param students:
    :return:
    """
    for student in students:
        reading_time = student["reading_time_list"]
        exercise_time = student["exercise_time_list"]
        tmp_list = []
        for i in range(7):

            tmp_list.append({"reading": _format_for_color(reading_time[i]),
                             "exercise": _format_for_color(exercise_time[i])})

        del student["reading_time_list"]
        del student["exercise_time_list"]

        student['time'] = tmp_list

    return students


def _format_for_color(time):
    """
    Part of the hotfix
    :param time:
    :return:
    """
    if 0 <= time <= 1:
        color = 0
    elif time < 3:
        color = 1
    elif time < 5:
        color = 2
    elif time < 7:
        color = 3
    else:
        color = 4

    return color