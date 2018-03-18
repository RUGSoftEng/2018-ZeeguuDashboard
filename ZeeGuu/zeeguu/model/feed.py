# -*- coding: utf8 -*-

import time
from datetime import datetime

import feedparser
import sqlalchemy.orm.exc
from sqlalchemy.orm.exc import NoResultFound

import zeeguu
from zeeguu.constants import JSON_TIME_FORMAT, SIMPLE_TIME_FORMAT
from zeeguu.model.language import Language
from zeeguu.model.url import Url

db = zeeguu.db


class RSSFeed(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'rss_feed'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(2083))
    description = db.Column(db.String(2083))

    language_id = db.Column(db.Integer, db.ForeignKey(Language.id))
    language = db.relationship(Language)

    url_id = db.Column(db.Integer, db.ForeignKey(Url.id))
    url = db.relationship(Url, foreign_keys=url_id)

    image_url_id = db.Column(db.Integer, db.ForeignKey(Url.id))
    image_url = db.relationship(Url, foreign_keys=image_url_id)

    last_crawled_time = db.Column(db.DateTime)

    def __init__(self, url, title, description, image_url=None, language=None):
        self.url = url
        self.image_url = image_url
        self.title = title
        self.language = language
        self.description = description
        self.last_crawled_time = datetime(2001, 1, 2)

    def __str__(self):
        language = "unknown"
        if self.language:
            language = self.language.code

        return f'{self.title, language}'

    def __repr__(self):
        return str(self)

    @classmethod
    def from_url(cls, url: str):
        data = feedparser.parse(url)

        try:
            title = data.feed.title
        except:
            title = ""

        try:
            description = data.feed.subtitle
        except:
            description = None

        try:
            image_url_string = data.feed.image.href
            print(f'Found image url at: {image_url_string}')
            image_url = Url(image_url_string, title + " Icon")
        except:
            print('Could not find any image url.')
            image_url = None

        feed_url = Url(url, title)

        return RSSFeed(feed_url, title, description, image_url, None)

        return RSSFeed()

    def as_dictionary(self):
        image_url = ""
        if self.image_url:
            image_url = self.image_url.as_string()

        language = "unknown_lang"
        if self.language:
            language = self.language.code

        return dict(
            id=self.id,
            title=self.title,
            url=self.url.as_string(),
            description=self.description,
            language=language,
            image_url=image_url
        )

    def feed_items(self):
        """

        :return: a dictionary with info about that feed
        extracted by feedparser
        and including: title, url, content, summary, time
        """

        def publishing_date(item):
            # this used to be updated_parsed but cf the deprecation
            # warning we changed to published_parsed instead.
            try:
                return item.published_parsed
            except:
                # March 8 -- added back in updated_parsed;
                # curious if this fixes the problem in some
                # cases; to find out, we log

                result = item.updated_parsed
                zeeguu.log(f'got updated_parsed where published_parsed failed for {item.get("link", "")}')
                return result

        feed_data = feedparser.parse(self.url.as_string())

        feed_items = []
        for item in feed_data.entries:
            try:
                new_item_data_dict = dict(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    content=item.get("content", ""),
                    summary=item.get("summary", ""),
                    published=time.strftime(SIMPLE_TIME_FORMAT, publishing_date(item))
                )
                feed_items.append(new_item_data_dict)

            except AttributeError as e:
                zeeguu.log(f'Exception {e} while trying to retrieve {item.get("link", "")}')

        return feed_items

    @classmethod
    def exists(cls, rss_feed):
        try:
            cls.query.filter(
                cls.url == rss_feed.url
            ).one()
            return True
        except NoResultFound:
            return False

    @classmethod
    def find_by_id(cls, i):
        try:
            result = cls.query.filter(cls.id == i).one()
            return result
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_url(cls, url):
        try:
            result = cls.query.filter(cls.url == url).one()
            return result
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    @classmethod
    def find_or_create(cls, session, url, title, description, image_url: Url, language: Language):
        try:
            result = (cls.query.filter(cls.url == url)
                      .filter(cls.title == title)
                      .filter(cls.language == language)
                      .filter(cls.description == description)
                      .one())
            return result
        except sqlalchemy.orm.exc.NoResultFound:
            new = cls(url, title, description, image_url, language)
            session.add(new)
            session.commit()
            return new

    # although it seems to not be used by anybody,
    # this method is being used from the zeeguu-api
    @classmethod
    def find_for_language_id(cls, language_code):
        language = Language.find(language_code)
        return cls.query.filter(cls.language == language).group_by(cls.title).all()

    def get_articles(self, user, limit=None, after_date=None, most_recent_first=False, easiest_first=False):
        """

            Articles for this feed from the article DB

        :param limit:
        :param after_date:
        :param most_recent_first:
        :param easiest_first:
        :return:
        """

        from zeeguu.model import Article

        if not after_date:
            after_date = datetime(2001, 1, 1)

        try:
            q = (Article.query.
                 filter(Article.rss_feed == self).
                 filter(Article.published_time >= after_date).
                 filter(Article.word_count > Article.MINIMUM_WORD_COUNT))

            if most_recent_first:
                q = q.order_by(Article.published_time.desc())
            if easiest_first:
                q = q.order_by(Article.fk_difficulty)

            return q.limit(limit).all()

        except Exception as e:
            raise (e)
            return None
