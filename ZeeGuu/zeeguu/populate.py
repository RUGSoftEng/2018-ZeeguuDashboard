# -*- coding: utf8 -*-
import datetime
import random
import re

from zeeguu.model.exercise import Exercise

from zeeguu.model.url import Url
from zeeguu.model.text import Text
from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.user_word import UserWord
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.language import Language
from zeeguu.model.user import User

WORD_PATTERN = re.compile("\[?([^{\[]+)\]?( {[^}]+})?( \[[^\]]\])?")

TEST_PASS = 'test'
TEST_EMAIL = 'i@mir.lu'

TEST_BOOKMARKS_COUNT = 2

def drop_current_tables(db):
    # We have to do a commit() before the drop_all()
    # Otherwise the system just freezes sometimes!
    db.session.commit()
    db.session.close_all()
    # Initial cleanup
    db.reflect()
    db.drop_all()
    # Creating the tables again
    db.create_all()


def add_bookmark(db, user, original_language, original_word, translation_language, translation_word, date, the_context,
                 the_url, the_url_title):
    session = db.session

    url = Url.find_or_create(session, the_url, the_url_title)

    text = Text.find_or_create(session, the_context, translation_language, url)

    origin = UserWord.find_or_create(session, original_word, original_language)

    translation = UserWord.find_or_create(session, translation_word, translation_language)

    b1 = Bookmark(origin, translation, user, text, date)
    db.session.add(b1)
    db.session.commit()

    return b1


#
def create_minimal_test_db(db):
    drop_current_tables(db)

    # Some common test fixtures
    de = Language("de", "German")
    en = Language("en", "English")
    nl = Language("nl", "Dutch")
    es = Language("es", "Spanish")
    fr = Language("fr", "French")

    db.session.add_all([en, de, nl, es, fr]);

    mir = User(TEST_EMAIL, "Mircea", TEST_PASS, de, en)

    db.session.add(mir)

    show_solution = ExerciseOutcome("Show solution")
    retry = ExerciseOutcome("Retry")
    correct = ExerciseOutcome("Correct")
    wrong = ExerciseOutcome("Wrong")
    typo = ExerciseOutcome("Typo")
    too_easy = ExerciseOutcome("Too easy")

    outcomes = [show_solution, retry, correct, wrong, typo, too_easy]

    db.session.add_all(outcomes)

    recognize = ExerciseSource("Recognize")
    translate = ExerciseSource("Translate")

    sources = [recognize, translate]

    db.session.add_all(sources)

    b1 = add_bookmark(db, mir, de, "Schaf", en, "sheep",
                      datetime.datetime(2011, 1, 1, 1, 1, 1),
                      "Bitte... zeichne mir ein Schaf!",
                      "http://www.derkleineprinz-online.de/text/2-kapitel/",
                      "Der Kleine Prinz - Kapitel 2")

    b2 = add_bookmark(db, mir, de, "sprang", en, "jumped",
                      datetime.datetime(2011, 1, 1, 1, 1, 1),
                      "Ich sprang auf die Fusse.",
                      "http://www.derkleineprinz-online.de/text/2-kapitel/",
                      "Der Kleine Prinz - Kapitel 2")

    bookmarks = [b1, b2]

    for i in range(0, 5):
        random_source = sources[random.randint(0, len(sources) - 1)]
        random_outcome = outcomes[random.randint(0, len(outcomes) - 1)]
        random_solving_speed = random.randint(500, 5000)
        exercise = Exercise(random_outcome, random_source,
                            random_solving_speed, datetime.datetime.now())
        random_bookmark = bookmarks[random.randint(0, len(bookmarks) - 1)]
        random_bookmark.add_new_exercise(exercise)

    global TEST_BOOKMARKS_COUNT
    TEST_BOOKMARKS_COUNT = 2
    db.session.commit()
