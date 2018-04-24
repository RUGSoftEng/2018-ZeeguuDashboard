import json

from app.api.api_connection import api_get


def load_user_info(user_id):
    student_info = api_get('user_info/'+str(user_id))
    return json.loads(student_info.text)


def load_user_data(user_id, filtered = True):
    stats_json = api_get("cohort_member_bookmarks/"+str(user_id)).text
    stats = json.loads(stats_json)
    return stats


def filter_user_bookmarks(dict):
    word_string = " "
    for day in dict:
        for bookmark in day["bookmar1ks"]:
            if bookmark["from"] in word_string:
                day["bookmarks"].remove(bookmark)
            else:
                word_string = bookmark["from"]
    return dict