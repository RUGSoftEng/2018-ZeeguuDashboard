from sqlalchemy.orm import relationship

import zeeguu

from sqlalchemy import Column, Integer, String, ForeignKey, and_

db = zeeguu.db


class Topic(db.Model):
    """

        A topic is one way of categorizing articles.
        Examples: #health #sports etc.

    """
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = Column(Integer, primary_key=True)

    name = Column(String(64))

    from zeeguu.model.language import Language

    language_id = Column(Integer, ForeignKey(Language.id))
    language = relationship(Language)

    # space separated patterns that when found in the url
    # hint that we have an article for the topic
    url_patterns = Column(String(1024))

    def __init__(self, name, language, url_patterns=""):
        self.name = name
        self.language = language
        self.url_patterns = url_patterns

    def __repr__(self):
        return f'<Topic {self.name} ({self.language})>'

    def matches_article(self, article):
        patterns = self.url_patterns.strip().split(" ")
        for each_pattern in patterns:
            if each_pattern in article.url.as_string():
                return True

        return False

    def all_articles(self):
        from zeeguu.model import Article

        return Article.query.filter(Article.topics.any(id=self.id)).all()

    @classmethod
    def find(cls, name: str, language: 'Language'):

        try:
            return (cls.query.filter(and_(cls.name == name, cls.language == language))).one()
        except:
            return None
