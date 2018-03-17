#
import datetime
import json
import random
import re

import sqlalchemy.orm
import zeeguu
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from zeeguu import util
from zeeguu.language.difficulty_estimator_factory import DifficultyEstimatorFactory
from zeeguu.model.language import Language

db = zeeguu.db


class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    EMAIL_VALIDATION_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    ANONYMOUS_EMAIL_DOMAIN = '@anon.zeeguu'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    invitation_code = db.Column(db.String(255))
    password = db.Column(db.String(255))
    password_salt = db.Column(db.String(255))
    learned_language_id = db.Column(
        db.Integer,
        db.ForeignKey(Language.id)
    )
    learned_language = relationship(Language, foreign_keys=[learned_language_id])

    native_language_id = db.Column(
        db.Integer,
        db.ForeignKey(Language.id)
    )
    native_language = relationship(Language, foreign_keys=[native_language_id])

    from zeeguu.model.cohort import Cohort
    cohort_id = Column(Integer, ForeignKey(Cohort.id))
    cohort = relationship(Cohort)

    def __init__(self, email, name, password, learned_language=None, native_language=None, invitation_code=None):
        self.email = email
        self.name = name
        self.update_password(password)
        self.learned_language = learned_language or Language.default_learned()
        self.native_language = native_language or Language.default_native_language()
        self.invitation_code = invitation_code

    @classmethod
    def create_anonymous(cls, uuid, password, learned_language_code=None, native_language_code=None):
        """j

        :param uuid:
        :param password:
        :param learned_language_code:
        :param native_language:
        :return:
        """

        # since the DB must have an email we generate a fake one
        fake_email = uuid + cls.ANONYMOUS_EMAIL_DOMAIN

        if learned_language_code is not None:
            try:
                learned_language = Language.find_or_create(learned_language_code)
            except NoResultFound as e:
                learned_language = None
        else:
            learned_language = None

        if native_language_code is not None:
            try:
                native_language = Language.find_or_create(native_language_code)
            except NoResultFound as e:
                native_language = None
        else:
            native_language = None

        new_user = cls(fake_email, uuid, password, learned_language=learned_language, native_language=native_language)

        # # Until we find_or_create a better way of adding exercises for anonymous and new users... we simply
        # from zeeguu.temporary.default_words import default_bookmarks
        # default_bookmarks(new_user, learned_language_code)

        return new_user

    def __repr__(self):
        return '<User %r>' % (self.email)

    def details_as_dictionary(self):
        return dict(
            email=self.email,
            name=self.name,
            learned_language=self.learned_language.code,
            native_language=self.native_language.code
        )

    def preferred_difficulty_estimator(self):
        """
        :return: Difficulty estimator from preferences,
        otherwise the default one which is FrequencyDifficultyEstimator
        """

        from zeeguu.model.user_preference import UserPreference
        # Must have this import here to avoid circular dependency

        preference = UserPreference.get_difficulty_estimator(self) or "FleschKincaidDifficultyEstimator"
        zeeguu.log(f"Difficulty estimator for user {self.id}: {preference}")
        return preference

    def text_difficulty(self, text, language):

        estimator = DifficultyEstimatorFactory.get_difficulty_estimator(self.preferred_difficulty_estimator())
        return estimator.estimate_difficulty(text, language, self)

    def set_learned_language(self, code):
        self.learned_language = Language.find(code)

    def set_native_language(self, code):
        self.native_language = Language.find(code)

    def has_bookmarks(self):
        return self.bookmark_count() > 0

    def date_of_last_bookmark(self):
        """
            assumes that there are bookmarks
        """
        return self.bookmarks_chronologically()[0].time

    def active_during_recent(self, days: int = 30):
        if not self.has_bookmarks():
            return False

        import dateutil.relativedelta
        now = datetime.datetime.now()
        a_while_ago = now - dateutil.relativedelta.relativedelta(days=days)
        return self.date_of_last_bookmark() > a_while_ago

    @classmethod
    @sqlalchemy.orm.validates("email")
    def validate_email(cls, col, email):
        if not re.match(cls.EMAIL_VALIDATION_REGEX, email):
            raise ValueError("Invalid email address")
        return email

    @classmethod
    @sqlalchemy.orm.validates("password")
    def validate_password(cls, col, password):
        if password is None or len(password) == 0:
            raise ValueError("Invalid password")
        return password

    @classmethod
    @sqlalchemy.orm.validates("name")
    def validate_name(cls, col, name):
        if name is None or len(name) == 0:
            raise ValueError("Invalid username")
        return name

    def update_password(self, password:str):
        """
        
        :param password: str
        :return: 
        """
        salt_bytes = "".join(chr(random.randint(0, 255)) for _ in range(32)).encode('utf-8')

        self.password = util.password_hash(password, salt_bytes)
        self.password_salt = salt_bytes.hex()

    def all_bookmarks(self, after_date=datetime.datetime(1970, 1, 1),
                      before_date=datetime.date.today() + datetime.timedelta(
                          days=1)):
        from zeeguu.model.bookmark import Bookmark
        return Bookmark.query. \
            filter_by(user_id=self.id). \
            filter(Bookmark.time >= after_date). \
            filter(Bookmark.time <= before_date). \
            order_by(Bookmark.time.desc()).all()

    def all_bookmarks_fit_for_study(self):
        from zeeguu.model.bookmark import Bookmark
        return Bookmark.query. \
            filter_by(user_id=self.id). \
            filter_by(fit_for_study=True).all()

    def bookmarks_chronologically(self):
        from zeeguu.model.bookmark import Bookmark
        return Bookmark.query.filter_by(user_id=self.id).order_by(
            Bookmark.time.desc()).all()

    def bookmarks_by_date(self, after_date=datetime.datetime(1970, 1, 1)):
        """

        :param after_date:
        :return: a pair of 1. a dict with date-> bookmarks and 2. a sorted list of dates
        """

        def extract_day_from_date(bookmark):
            return bookmark, bookmark.time.replace(bookmark.time.year,
                                                   bookmark.time.month,
                                                   bookmark.time.day, 0, 0, 0,
                                                   0)

        bookmarks = self.all_bookmarks(after_date)
        bookmarks_by_date = dict()

        for elem in map(extract_day_from_date, bookmarks):
            bookmarks_by_date.setdefault(elem[1], []).append(elem[0])

        sorted_dates = list(bookmarks_by_date.keys())
        sorted_dates.sort(reverse=True)
        return bookmarks_by_date, sorted_dates

    def bookmarks_by_day(self, with_context,
                         after_date=datetime.datetime(2010, 1, 1)):
        bookmarks_by_date, sorted_dates = self.bookmarks_by_date(after_date)

        dates = []
        for date in sorted_dates:
            bookmarks = []
            for bookmark in bookmarks_by_date[date]:
                bookmarks.append(bookmark.json_serializable_dict(with_context))
            date_entry = dict(
                date=date.strftime("%A, %d %B %Y"),
                bookmarks=bookmarks
            )
            dates.append(date_entry)
        return dates

    def bookmarks_by_url_by_date(self, n_days=365):
        bookmarks_list, dates = self.bookmarks_by_date()

        most_recent_n_days = dates[0:n_days]

        urls_by_date = {}
        texts_by_url = {}
        for date in most_recent_n_days:
            for bookmark in bookmarks_list[date]:
                urls_by_date.setdefault(date, set()).add(bookmark.text.url)
                texts_by_url.setdefault(bookmark.text.url, set()).add(bookmark.text)
        return most_recent_n_days, urls_by_date, texts_by_url

    def bookmarks_to_study(self, bookmark_count=10, generate_bookmarks_if_needed=False):
        """

        :param bookmark_count: by default we recommend 10 words

        :param generate_bookmarks_if_needed: force generating some example words, even if
            there are none in the history of the user. Before this param was introduced,
             the system would always generate some examples here...
        :return:
        """
        from zeeguu.word_scheduling import arts

        bookmarks = arts.bookmarks_to_study(self, bookmark_count, zeeguu.db)

        if len(bookmarks) == 0 and self.bookmark_count() == 0 and generate_bookmarks_if_needed:
            # we have zero bookmarks in our account... better to generate some
            # bookmarks to study than just whistle...
            # we might be in a situation where we're on the watch for example...
            # in this case, we add some new ones to the user's account
            from zeeguu.temporary.default_words import create_default_bookmarks
            new_bookmarks = create_default_bookmarks(zeeguu.db.session, self, self.learned_language.code)

            for each_new in new_bookmarks:
                # try to find if the user has seen this in the past
                bookmarks.append(each_new)
                zeeguu.db.session.add(each_new)

                if len(bookmarks) == bookmark_count:
                    break

            zeeguu.db.session.commit()

        return bookmarks

    def bookmark_counts_by_date(self):
        """returns array with added bookmark amount per each date for the last year
        this function is for the activity_graph, generates data
        """

        # compute bookmark_counts_by_date
        year = datetime.date.today().year - 1  # get data from year 2015(if this year is 2016)
        month = datetime.date.today().month
        bookmarks_dict, dates = self.bookmarks_by_date(
            datetime.datetime(year, month, 1))

        counts = []
        for date in dates:
            the_date = date.strftime('%Y-%m-%d')
            the_count = len(bookmarks_dict[date])
            counts.append(dict(date=the_date, count=the_count))

        bookmark_counts_by_date = json.dumps(counts)
        return bookmark_counts_by_date

    def learner_stats_data(self):
        """returns array with learned and learning words count per each month for the last year
        this function is for the line_graph, generates data
        """

        # compute learner_stats_data
        from zeeguu.model.learner_stats.learner_stats import \
            compute_learner_stats
        learner_stats_data = compute_learner_stats(self)

        return learner_stats_data

    def user_words(self):
        return [b.origin.word for b in self.all_bookmarks()]

    def bookmark_count(self):
        return len(self.all_bookmarks())

    def word_count(self):
        return len(self.user_words())

    @classmethod
    def find_all(cls):
        return User.query.all()

    @classmethod
    def find(cls, email):
        return User.query.filter(User.email == email).one()

    @classmethod
    def find_by_id(cls, id):
        return User.query.filter(User.id == id).one()

    @classmethod
    def exists(cls, user):
        try:
            cls.query.filter_by(
                email=user.email,
                id=user.id
            ).one()
            return True
        except NoResultFound:
            return False

    @classmethod
    def authorize(cls, email, password):
        try:
            user = cls.query.filter(cls.email == email).one()
            if user.password == util.password_hash(password, bytes.fromhex(user.password_salt)):
                return user
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def authorize_anonymous(cls, uuid, password):
        email = uuid + cls.ANONYMOUS_EMAIL_DOMAIN
        return cls.authorize(email, password)
