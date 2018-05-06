import json

from app.api import api_connection


# This file contains all of the utility functions for loading and formatting user data.


def load_user_info(user_id):
    student_info = api_connection.api_get('user_info/' + str(user_id))
    return json.loads(student_info.text)


def load_user_data(user_id, filtered=True):
    stats_json = api_connection.api_get("cohort_member_bookmarks/" + str(user_id)).text
    stats = json.loads(stats_json)
    return stats


def filter_user_bookmarks(dict):
    word_string = " "
    for day in dict:
        for bookmark in day["bookmarks"]:
            if bookmark["from"] in word_string:
                day["bookmarks"].remove(bookmark)
            else:
                word_string = bookmark["from"]
    return dict
