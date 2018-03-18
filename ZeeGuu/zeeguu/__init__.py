# -*- coding: utf8 -*-
import os

import datetime

LOGS_FOLDER = '~/.logs'

log_dir = os.path.expanduser(LOGS_FOLDER)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.expanduser(f"{LOGS_FOLDER}/zeeguu.log")


def log(text):
    text = f'{datetime.datetime.now()} {text}'

    with open(log_file, "a", encoding='utf-8') as file:
        file.write(f'{text}\n')
    return text


def log_n_print(text):
    """

        Print both to stdout and the logfile

    :return: None
    """
    print(log(text))
