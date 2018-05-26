import json

from app.api.api_connection import api_get

"""
This file contains all of the utility functions for loading and formatting user data.
"""


def get_correct_time(time):
    """
    Returns correct string according to time given as a string
    :param time:
    :return:
    """

    if time == '7':
        return "1 Week"
    elif time == '14':
        return "2 Weeks"
    elif time == '30':
        return "1 Month"
    elif time == '180':
        return "6 Months"
    elif time == '365':
        return "1 Year"


def load_user_info(user_id, duration):
    """
    Loads an invidiual users data.
    Requires permission (the logged in teacher must be a teacher of the class containing user with user_id ).
    :param user_id: user_id used to find user.
    :return: Dictionary containing (id, name, email, reading time, exercises done, last article)
    """
    student_info = api_get('user_info/' + str(user_id) + "/" + str(duration))
    return json.loads(student_info.text)


def load_user_data(user_id, time, filtered=True):
    """
    Function to load user statistics (bookmarks).
    :param user_id: used to find user
    :param time: duration in which to collect bookmarks from.
    :param filtered: is this data being filtered
    :return: Dictionary of bookmarks.
    """
    stats_json = api_get("cohort_member_bookmarks/" + str(user_id) + "/" + str(time)).text
    stats = json.loads(stats_json)
    if filtered is True:
        stats = filter_user_bookmarks(stats)
    return stats


def filter_user_bookmarks(dict):
    """
    Function to filter bookmarks.
    :param dict: this is the unfiltered bookmarks
    :return: Dictionary of bookmarks where duplicated entries are removed.
    """
    word_string = " "
    for day in dict:
        for bookmark in day["bookmarks"]:
            if bookmark["from"] in word_string:
                day["bookmarks"].remove(bookmark)
            else:
                word_string = bookmark["from"]
    return dict
