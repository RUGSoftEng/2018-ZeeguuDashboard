import re
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from wordstats import Word

import zeeguu
from zeeguu.model.exercise import Exercise
from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.language import Language
from zeeguu.model.text import Text
from zeeguu.model.url import Url
from zeeguu.model.user import User
from zeeguu.model.user_word import UserWord
from zeeguu.util.timer_logging_decorator import time_this

db = zeeguu.db

bookmark_exercise_mapping = Table('bookmark_exercise_mapping',
                                  db.Model.metadata,
                                  Column('bookmark_id', Integer,
                                         ForeignKey('bookmark.id')),
                                  Column('exercise_id', Integer,
                                         ForeignKey('exercise.id'))
                                  )

WordAlias = db.aliased(UserWord, name="translated_word")


class Bookmark(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)

    origin_id = db.Column(db.Integer, db.ForeignKey(UserWord.id), nullable=False)
    origin = db.relationship(UserWord, primaryjoin=origin_id == UserWord.id)

    translation_id = db.Column(db.Integer, db.ForeignKey(UserWord.id), nullable=False)
    translation = db.relationship(UserWord, primaryjoin=translation_id == UserWord.id)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    text_id = db.Column(db.Integer, db.ForeignKey(Text.id))
    text = db.relationship(Text)

    time = db.Column(db.DateTime)

    exercise_log = relationship(Exercise,
                                secondary="bookmark_exercise_mapping",
                                order_by="Exercise.id")

    starred = db.Column(db.Boolean, default=False)

    learned = db.Column(db.Boolean, default=False)

    fit_for_study = db.Column(db.Boolean)

    learned_time = db.Column(db.DateTime)

    def __init__(self, origin: UserWord, translation: UserWord, user: 'User',
                 text: str, time: datetime):
        self.origin = origin
        self.translation = translation
        self.user = user
        self.time = time
        self.text = text
        self.stared = False
        self.fit_for_study = self._fit_for_study()

    def __repr__(self):
        return "Bookmark[{3} of {4}: {0}->{1} in '{2}...']\n". \
            format(self.origin.word, self.translation.word,
                   self.text.content[0:10], self.id, self.user_id)

    def serializable_dictionary(self):
        return dict(
            origin=self.origin.word,
            translation=self.translation.word,
            context=self.text.content
        )

    def add_new_exercise(self, exercise):
        self.exercise_log.append(exercise)

    def translations_rendered_as_text(self):
        return self.translation.word

    def content_is_not_too_long(self):
        return len(self.text.content) < 60

    def events_prevent_further_study(self):
        from zeeguu.model.smartwatch.watch_interaction_event import \
            WatchInteractionEvent
        events_for_self = WatchInteractionEvent.events_for_bookmark(self)
        return any([x.prevents_further_study() for x in events_for_self])

    def origin_same_as_translation(self):
        try:
            return self.origin.word.lower() == self.translation.word.lower()
        except:
            print("missing word for bookmark with id {0}".format(self.id))
            return False

    def is_subset_of_larger_bookmark(self):
        """
            if the user translates a superset of this sentence
        """
        all_bookmarks_in_text = Bookmark.find_all_for_user_and_text(self.user, self.text)
        for each in all_bookmarks_in_text:
            if each != self:
                if self.origin.word in each.origin.word:
                    return True
        return False

    def multiword_origin(self):
        return len(self.origin.word.split(" ")) > 1

    def origin_word_count(self):
        return len(self.origin.word.split(" "))

    def quality_bookmark(self):

        # If it's starred by the user, then it's good quality!
        if self.starred:
            zeeguu.log("starred -> good quality")
            return True

        # Else it just should not be bad quality!
        return not self.bad_quality_bookmark()

    def translation_in_context(self):
        if self.translation.word in self.text.content:
            return True

    def bad_quality_bookmark(self):
        # following are reasons that disqualify a bookmark from
        bad_quality = (

            # translation is same as origin
                self.origin_same_as_translation() or

                # origin which is subset of a larger origin
                (self.is_subset_of_larger_bookmark()) or

                # too long for our exercises
                (self.origin_word_count() > 3) or

                # very short words are also not great quality
                (len(self.origin.word) < 3)

                or
                # a too long context is not good either
                self.context_word_count() > 20

                or
                # a superset of translation same as origin...
                # happens in the case of some bugs in translation
                # where the translation is inserted in the text
                # till we fix it, we should not show this
                self.translation_in_context()

        )

        return bad_quality

    def update_fit_for_study(self, session):
        """
            Called when something happened to the bookmark,
             that requires it's "fit for study" status to be
              updated.
        :param session:
        :return:
        """
        self.fit_for_study = self._fit_for_study()
        session.add(self)

    @time_this
    def _fit_for_study(self):

        """

            A bookmark is good for study if it respects several
            properties:

            - has not been learned already
            - is a quality bookmark (which includes those starred by the user)
            - there's no feedback from the user that prevents us from showing it
            - the last outcome is not "too easy"

        :return:
        """

        last_outcome = self.latest_exercise_outcome()

        if last_outcome is None:
            return self.quality_bookmark() and not self.events_prevent_further_study()

        if self.is_learned_based_on_exercise_outcomes():
            return False

        return (self.quality_bookmark() and
                not last_outcome.too_easy() and
                not last_outcome.unknown_feedback() and
                not self.events_prevent_further_study())

    def add_new_exercise_result(self, exercise_source, exercise_outcome,
                                exercise_solving_speed):
        new_source = ExerciseSource.query.filter_by(
            source=exercise_source.source
        ).first()
        new_outcome = ExerciseOutcome.query.filter_by(
            outcome=exercise_outcome.outcome
        ).first()
        exercise = Exercise(new_outcome, new_source, exercise_solving_speed,
                            datetime.now())
        self.add_new_exercise(exercise)
        db.session.add(exercise)

    def split_words_from_context(self):

        result = []
        bookmark_content_words = re.findall(r'(?u)\w+', self.text.content)
        for word in bookmark_content_words:
            if word.lower() != self.origin.word.lower():
                result.append(word)

        return result

    def context_word_count(self):
        words = self.split_words_from_context()
        return len(words)

    def json_serializable_dict(self, with_context=True):
        try:
            translation_word = self.translation.word
        except AttributeError as e:
            translation_word = ''
            zeeguu.log(f"Exception caught: for some reason there was no translation for {self.id}")
            print(str(e))

        result = dict(
            id=self.id,
            to=translation_word,
            from_lang=self.origin.language.code,
            to_lang=self.translation.language.code,
            title=self.text.url.title,
            url=self.text.url.as_string(),
            origin_importance=Word.stats(self.origin.word,
                                         self.origin.language.code).importance
        )
        result["from"] = self.origin.word
        if with_context:
            result['context'] = self.text.content
        return result

    @classmethod
    def find_or_create(cls, session, user,
                       _origin: str, _origin_lang: str,
                       _translation: str, _translation_lang: str,
                       _context: str, _url: str, _url_title: str):
        """
            if the bookmark does not exist, it creates it and returns it
            if it exists, it ** updates the translation** and returns the bookmark object

        :param _origin:
        :param _context:
        :param _url:
        :return:
        """

        origin_lang = Language.find_or_create(_origin_lang)
        translation_lang = Language.find_or_create(_translation_lang)

        origin = UserWord.find_or_create(session, _origin, origin_lang)

        url = Url.find_or_create(session, _url, _url_title)

        context = Text.find_or_create(session, _context, origin_lang, url)

        translation = UserWord.find_or_create(session, _translation, translation_lang)

        now = datetime.now()

        try:
            # try to find this bookmark
            bookmark = Bookmark.find_by_user_word_and_text(user, origin,
                                                           context)

            # update the translation
            bookmark.translation = translation

        except sqlalchemy.orm.exc.NoResultFound as e:
            bookmark = cls(origin, translation, user, context, now)
        except Exception as e:
            raise e

        session.add(bookmark)
        session.commit()

        return bookmark

    @classmethod
    def find_by_specific_user(cls, user):
        return cls.query.filter_by(
            user=user
        ).all()

    @classmethod
    def find_all(cls):
        return cls.query.filter().all()

    @classmethod
    def find_all_for_user_and_text(cls, text, user):
        return cls.query.filter_by(text=text, user=user).all()

    @classmethod
    def find_all_for_user_and_url(cls, user, url):
        return cls.query.join(Text).filter(Text.url == url).filter(Bookmark.user == user).all()

    @classmethod
    def find(cls, b_id):
        return cls.query.filter_by(
            id=b_id
        ).one()

    @classmethod
    def find_all_by_user_and_word(cls, user, word):
        return cls.query.filter_by(
            user=user,
            origin=word
        ).all()

    @classmethod
    def find_by_user_word_and_text(cls, user, word, text):
        return cls.query.filter_by(
            user=user,
            origin=word,
            text=text
        ).one()

    @classmethod
    def exists(cls, bookmark):
        try:
            cls.query.filter_by(
                origin_id=bookmark.origin.id,
                id=bookmark.id
            ).one()
            return True
        except NoResultFound:
            return False

    def latest_exercise_outcome(self):
        sorted_exercise_log_by_latest = sorted(self.exercise_log,
                                               key=lambda x: x.time,
                                               reverse=True)
        if sorted_exercise_log_by_latest:
            return sorted_exercise_log_by_latest[0].outcome
        else:
            return None

    def sorted_exercise_log(self):
        return sorted(self.exercise_log,
                      key=lambda x: x.time,
                      reverse=True)

    def check_if_learned_based_on_exercise_outcomes(self,
                                                    add_to_result_time=False):
        """
        TODO: This should replace check_is_latest_outcome in the future...
        :param add_to_result_time:
        :return:
        """
        if len(self.exercise_log) == 0:
            if add_to_result_time:
                return False, None

            return False

        last_exercise = self.exercise_log[-1]

        # If last outcome is TOO EASY we know it
        if last_exercise.outcome.outcome == ExerciseOutcome.TOO_EASY:
            if add_to_result_time:
                return True, last_exercise.time

            return True

        CORRECTS_IN_A_ROW = 5
        if len(self.exercise_log) >= CORRECTS_IN_A_ROW:

            # If we got it right for the last CORRECTS_IN_A_ROW times, we know it
            if all(exercise.outcome.correct for exercise in self.exercise_log[-CORRECTS_IN_A_ROW:]):
                return True, last_exercise.time

        if add_to_result_time:
            return False, None

        return False

    def is_learned_based_on_exercise_outcomes(self,
                                              also_return_time=False):
        """
        TODO: This should replace check_is_latest_outcome in the future...

        :param also_return_time:
        :return:
        """
        sorted_exercise_log_by_latest = self.sorted_exercise_log()

        if sorted_exercise_log_by_latest:
            last_exercise = sorted_exercise_log_by_latest[0]

            # If last outcome is TOO EASY we know it
            if last_exercise.outcome.outcome == ExerciseOutcome.TOO_EASY:
                if also_return_time:
                    return True, last_exercise.time
                return True

            CORRECTS_IN_A_ROW = 5
            if len(sorted_exercise_log_by_latest) > CORRECTS_IN_A_ROW:

                # If we got it right for the last CORRECTS_IN_A_ROW times, we know it
                if all(exercise.outcome.outcome == ExerciseOutcome.CORRECT for
                       exercise in
                       sorted_exercise_log_by_latest[0:CORRECTS_IN_A_ROW - 1]):
                    return True, last_exercise.time

        if also_return_time:
            return False, None
        return False

    def update_learned_status(self, session):
        """
            To call when something happened to the bookmark,
             that requires it's "learned" status to be updated.
        :param session:
        :return:
        """
        is_learned, learned_time = self.is_learned_based_on_exercise_outcomes(True)
        log = self.sorted_exercise_log()
        exercise_log_summary = ' '.join([exercise.short_string_summary() for exercise in log])
        if is_learned:
            zeeguu.log(f"Log: {exercise_log_summary}: bookmark {self.id} learned!")
            self.learned_time = learned_time
            self.learned = True
            session.add(self)
        else:
            zeeguu.log(f"Log: {exercise_log_summary}: bookmark {self.id} not learned yet.")

    def events_indicate_its_learned(self):
        from zeeguu.model.smartwatch.watch_interaction_event import \
            WatchInteractionEvent
        events_for_self = WatchInteractionEvent.events_for_bookmark(self)

        for event in events_for_self:
            if event.is_learned_event():
                return True, event.time

        return False, None

    def has_been_learned(self, also_return_time=False):
        # TODO: This must be stored in the DB together with the
        # bookmark... once a bookmark has been learned, we should
        # not not need to doubt it ... we might still want to confirm
        # say one month later, or three months later...

        """
        :param also_return_time: should the function return also the time when
        the bookmark has been learned?

        :return: boolean indicating whether the bookmark has already been learned,
        togetgher with the time when it was learned if also_return_time is set
        """

        # The first case is when we have an exercise outcome set to Too EASY
        learned, time = self.is_learned_based_on_exercise_outcomes(True)
        if learned:
            if also_return_time:
                return True, time

            return True

        # The second case is when we have an event in the smartwatch event log
        # that indicates that the word has been learned
        learned, time = self.events_indicate_its_learned()
        if learned:
            return learned, time

        if also_return_time:
            return False, None

        return False
