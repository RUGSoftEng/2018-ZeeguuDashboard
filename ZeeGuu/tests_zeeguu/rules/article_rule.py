from datetime import datetime, timedelta
from random import randint

from tests_zeeguu.rules.base_rule import BaseRule
from tests_zeeguu.rules.language_rule import LanguageRule
from tests_zeeguu.rules.rss_feed_rule import RSSFeedRule
from tests_zeeguu.rules.url_rule import UrlRule
from zeeguu.model import Article


class ArticleRule(BaseRule):
    """

        Creates an Article object with random data and saves it to the database.

    """

    def __init__(self):
        super().__init__()

        self.article = self._create_model_object()

        self.save(self.article)

    def _create_model_object(self):
        title = " ".join(self.faker.text().split()[:4])
        authors = self.faker.name()
        content = self.faker.text()
        summary = self.faker.text()
        published = datetime.now() - timedelta(minutes=randint(0, 7200))
        rss_feed = RSSFeedRule().feed
        language = LanguageRule().random
        url = UrlRule().url

        article = Article(url, title, authors, content, summary, published, rss_feed, language)

        if self._exists_in_db(article):
            return self._create_model_object()

        return article

    @staticmethod
    def _exists_in_db(obj):
        return Article.exists(obj)
