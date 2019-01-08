import json

from zeeguu_teacher_dashboard.api.api_connection import api_get

"""
This file contains all of the utility functions for loading and formatting user data.
"""


def human_readable_time(time):
    """
    Returns correct string according to time given as a string
    :param time:
    :return:
    """
    if time == '7':
        return "1 week"
    elif time == '14':
        return "2 weeks"
    elif time == '30':
        return "1 month"
    elif time == '180':
        return "6 months"
    elif time == '365':
        return "1 year"


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
        stats = sort_user_bookmarks(stats)
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


def sort_user_bookmarks(info_list):
    """
    Function to sort user bookmarks into order.
    :param info_list: this is the unsorted bookmarks list.
    :return: The sorted version of list of dictionary of bookmarks.
    """
    master_list = list()
    for element in info_list:
        master_element = dict()
        master_element['date'] = element['date']
        master_element['article_list'] = list()
        master_list.append(master_element)
        for bookmark in element['bookmarks']:
            exists_article = False
            for article in master_element['article_list']:
                if article['title'] == bookmark['title']:
                    exists_article = True
                    exists_sentence = False
                    for sentence in article['sentence_list']:
                        if sentence['context'] == bookmark['context']:
                            exists_sentence = True
                            sentence['bookmarks'].append(bookmark)
                    if exists_sentence is False:
                        sentence_element = dict()
                        sentence_element['context'] = bookmark['context']
                        sentence_element['bookmarks'] = list()
                        sentence_element['bookmarks'].append(bookmark)
                        article['sentence_list'].append(sentence_element)
            if exists_article is False:
                article_element = dict()
                article_element['title'] = bookmark['title']
                article_element['url'] = bookmark['url']
                article_element['sentence_list'] = list()
                master_element['article_list'].append(article_element)
                sentence_element = dict()
                sentence_element['context'] = bookmark['context']
                sentence_element['bookmarks'] = list()
                article_element['sentence_list'].append(sentence_element)
                sentence_element['bookmarks'].append(bookmark)
    return master_list

