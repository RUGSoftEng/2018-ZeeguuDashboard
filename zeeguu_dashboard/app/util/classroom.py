import json

from app.api.api_connection import api_post, api_get


"""
This file contains all of the utility functions required to get and format the data for the classroom page,
as well as posting data and changing it.
"""


def create_class(name, inv_code, max_students, language_id):
    """

    :param name:
    :param inv_code:
    :param max_students:
    :param language_id:
    :return:
    """
    package = {'name': name, 'inv_code': inv_code, 'max_students': max_students,
               'language_id': language_id}
    api_post('create_own_cohort', package)


def remove_class(class_id):
    """

    :param class_id:
    :return:
    """
    api_post('remove_cohort/' + str(class_id))


def load_class_info(class_id):
    """

    :param class_id:
    :return:
    """
    returned_class_infos_string = api_get("cohort_info/" + str(class_id)).text
    returned_class_info = json.loads(returned_class_infos_string)
    class_info = returned_class_info
    return class_info


def load_classes():
    """

    :return:
    """
    returned_class_infos_string = api_get("cohorts_info").text
    returned_class_infos = json.loads(returned_class_infos_string)
    classes = returned_class_infos
    return classes


def load_students(class_id):
    """

    :param class_id:
    :return:
    """
    returned_student_infos_string = api_get("users_from_cohort/" + str(class_id)).text
    returned_student_infos = json.loads(returned_student_infos_string)
    students = returned_student_infos
    return students


def verify_invite_code_exists(inv_code):
    """

    :param inv_code:
    :return:
    """
    inv_code_bool = api_get('invite_code_usable/' + str(inv_code)).text
    if inv_code_bool == "OK":
        return False
    return True
