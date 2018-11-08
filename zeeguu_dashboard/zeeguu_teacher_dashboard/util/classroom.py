import json
from datetime import datetime, timedelta

from zeeguu_teacher_dashboard.api.api_connection import api_post, api_get

"""
This file contains all of the utility functions required to get and format the data for the classroom page,
as well as posting data and changing it.
"""


def format_class_table_data(student_data, duration):
    """
    This function formats the data for the github style tables correctly to be displayed
    in the front-end.
    :param student_data:
    :param duration:
    :return:
    """
    now = datetime.today()
    duration = int(duration)
    student_times = []
    ideal_days = []
    for i in range(duration):
        ideal_days.append((now - timedelta(days=i)).strftime("%d-%m"))
    student_times.append(ideal_days)

    for s in student_data:
        day_list = []
        for day in range(0, duration):
            day_dictionary = {
                "date": now.strftime("%d-%m"),
                "reading": s.get("reading_time_list")[day],
                "exercise": s.get("exercise_time_list")[day],
                "reading_color": _format_for_color(s.get("reading_time_list")[day]),
                "exercise_color": _format_for_color(s.get("exercise_time_list")[day])
            }
            day_list.append(day_dictionary)
            now = now - timedelta(days=1);
        student_dictionary = {"name": s.get("name"), "day_list": day_list}
        student_times.append(student_dictionary)
    return student_times


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


def get_general_cohort_info(class_id):
    """
    Function for loading class information. Loads information in JSON format and converts it to dictionary.
    Requires permission (the logged in user must have permission to class)
    :param class_id:
    :return: Dictionary of class information (id, name, language_id, cur_students, max_students)
    """

    returned_class_infos_string = api_get("cohort_info/" + str(class_id)).text
    returned_class_info = json.loads(returned_class_infos_string)
    class_info = returned_class_info
    return class_info


def update_class_info(class_id, name, invite_code, declared_level_min, declared_level_max):
    """
    Function for editing class information. Makes an API call with the proper data.
    :param class_id: The id number of the class.
    :param name: The name of the class.
    :param invite_code: The invite code of the class for students to join.
    :param max_students: The maximum number of student
    :return:
    """
    package = {'name': name, 'inv_code': invite_code, 'declared_level_min': declared_level_min,
               'declared_level_max': declared_level_max}
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


def load_students(class_id, duration):
    """
    Function for loading information on all students in a class. Loads information in JSON format and converts it to a dictionary.
    Requires permission  ( the logged in user must have permission to view class that student is in)
    :param class_id:
    :return: Dictionary of dictionaries containing (id, name, email, reading time, exercises done, last article)
    """
    returned_student_infos_string = api_get("users_from_cohort/" + str(class_id) + "/" + str(duration)).text
    returned_student_infos = json.loads(returned_student_infos_string)
    students = returned_student_infos
    return students


def add_student_learning_proportion(students):
    """
    The function adds the "learning_proportion" for each student dictionary in the list of students,
    which tells the user how much reading compared to doing exercises did the student do.
    :param students: List of student dictionaries contiaing all of the relevant information about students
    to be displayed on the class page.
    :return: Same list with added element "learning_proportion" for each student dictionary.
    """
    for student in students:
        student["learning_proportion"] = 100
        if not (student["reading_time"] == 0 and student["exercises_done"] == 0):
            student["learning_proportion"] = 100 * student["reading_time"] / (
                    student["exercises_done"] + student["reading_time"])
        elif student["reading_time"] == 0 and student["exercises_done"] == 0:
            student["learning_proportion"] = 0
        elif student["reading_time"] == 0:
            student["learning_proportion"] = 0
        else:
            student["learning_proportion"] = 100
    return students


def add_total_and_normalized_time(students):
    max_activity = 0
    for student in students:
        student_total = student['exercises_done'] + student['reading_time']
        student['total_time'] = student_total
        if student_total > max_activity:
            max_activity = student_total

    if max_activity > 0:
        for student in students:
            student_total = student['exercises_done'] + student['reading_time']
            student['normalized_activity_proportion'] = student_total / max_activity * 100


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


def _format_for_color(time):
    """
    Part of the hotfix
    :param time:
    :return:
    """
    if time <= 1:
        color = 0
    elif time < 300:
        color = 1
    elif time < 600:
        color = 2
    elif time < 900:
        color = 3
    else:
        color = 4

    return color
