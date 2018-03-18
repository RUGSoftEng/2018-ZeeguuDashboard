import time

import sqlalchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

import zeeguu

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UnicodeText, Table

from zeeguu.constants import JSON_TIME_FORMAT
from zeeguu.language.difficulty_estimator_factory import DifficultyEstimatorFactory
from langdetect import detect

db = zeeguu.db

article_topic_mapping = Table('article_topic_mapping',
                              db.Model.metadata,
                              Column('article_id', Integer,
                                     ForeignKey('article.id')),
                              Column('topic_id', Integer,
                                     ForeignKey('topic.id'))
                              )


class Article(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = Column(Integer, primary_key=True)

    title = Column(String(512))
    authors = Column(UnicodeText)
    content = Column(UnicodeText())
    summary = Column(UnicodeText)
    word_count = Column(Integer)
    published_time = Column(DateTime)
    fk_difficulty = Column(Integer)

    from zeeguu.model.url import Url

    from zeeguu.model.feed import RSSFeed

    from zeeguu.model.language import Language

    rss_feed_id = Column(Integer, ForeignKey(RSSFeed.id))
    rss_feed = relationship(RSSFeed)

    url_id = Column(Integer, ForeignKey(Url.id), unique=True)
    url = relationship(Url)

    language_id = Column(Integer, ForeignKey(Language.id))
    language = relationship(Language)

    from zeeguu.model.topic import Topic
    topics = relationship(Topic,
                          secondary=article_topic_mapping,
                          backref=backref('articles'))

    # Few words in an article is very often not an
    # actul article but the caption for a video / comic.
    # Or maybe an article that's behind a paywall and
    # has only the first paragraph available
    MINIMUM_WORD_COUNT = 90

    def __init__(self, url, title, authors, content, summary, published_time, rss_feed, language):
        self.url = url
        self.title = title
        self.authors = authors
        self.content = content
        self.summary = summary
        self.published_time = published_time
        self.rss_feed = rss_feed
        self.language = language

        fk_estimator = DifficultyEstimatorFactory.get_difficulty_estimator("fk")
        fk_difficulty = fk_estimator.estimate_difficulty(self.content, self.language, None)['normalized']

        # easier to store integer in the DB
        # otherwise we have to use Decimal, and it's not supported on all dbs
        self.fk_difficulty = int(fk_difficulty * 100)
        self.word_count = len(self.content.split())

    def __repr__(self):
        return f'<Article {self.title} (w: {self.word_count}, d: {self.fk_difficulty}) ({self.url})>'

    def article_info(self, with_content=False):
        """

            This is the data that is sent over the API
            to the Reader. Whatever the reader needs
            must be here.

        :return:
        """

        result_dict = dict(
            id=self.id,
            title=self.title,
            url=self.url.as_string(),
            summary=self.summary,
            language=self.language.code,
            authors=self.authors,
            metrics=dict(
                difficulty=self.fk_difficulty / 100,
                word_count=self.word_count
            ))

        if self.published_time:
            result_dict['published'] = self.published_time.strftime(JSON_TIME_FORMAT)

        if self.rss_feed:
            result_dict['feed_id'] = self.rss_feed.id,
            result_dict['feed_image_url'] = self.rss_feed.image_url.as_string(),

        if with_content:
            result_dict['content'] = self.content

        return result_dict

    def add_topic(self, topic):
        self.topics.append(topic)

    def star_for_user(self, session, user, state=True):
        from zeeguu.model.user_article import UserArticle
        ua = UserArticle.find_or_create(session, user, self)
        ua.set_starred(state)
        session.add(ua)

    @classmethod
    def find_or_create(cls, session, url, language=None):
        """

            If not found, download and extract all
            the required info for this article.

        :param url:
        :return:
        """

        from zeeguu.model import Url, Article, Language
        import newspaper

        try:
            found = cls.find(url)
            if found:
                return found

            art = newspaper.Article(url=url)
            art.download()
            art.parse()

            if not language:
                if art.meta_lang == '':
                    art.meta_lang = detect(art.text)
                    zeeguu.log(f"langdetect: {art.meta_lang} for {url}")
                language = Language.find_or_create(art.meta_lang)

            # Create new article and save it to DB
            new_article = Article(
                Url.find_or_create(session, url),
                art.title,
                ', '.join(art.authors),
                art.text,
                art.summary,
                None,
                None,
                language
            )
            session.add(new_article)
            session.commit()
            return new_article
        except sqlalchemy.exc.IntegrityError or sqlalchemy.exc.DatabaseError:
            for i in range(10):
                try:
                    session.rollback()
                    u = cls.find(url)
                    print("Found article by url after recovering from race")
                    return u
                except:
                    print("Exception of second degree in article..." + str(i))
                    time.sleep(0.3)
                    continue
                break
        except Exception as e:
            import traceback
            traceback.print_exc()

    @classmethod
    def find(cls, url: str):
        """

            Find by url

        :return: object or None if not found
        """

        from zeeguu.model import Url
        try:
            url_object = Url.find(url)
            return (cls.query.filter(cls.url == url_object)).one()
        except NoResultFound:
            return None

    @classmethod
    def exists(cls, article):
        try:
            cls.query.filter(
                cls.url == article.url
            ).one()
            return True
        except NoResultFound:
            return False
