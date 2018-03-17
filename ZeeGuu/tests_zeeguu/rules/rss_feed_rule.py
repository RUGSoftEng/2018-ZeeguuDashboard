from datetime import datetime, timedelta
from random import randint

from tests_zeeguu.rules.base_rule import BaseRule
from tests_zeeguu.rules.language_rule import LanguageRule
from tests_zeeguu.rules.url_rule import UrlRule
from zeeguu.model import RSSFeed, Language, Url

URL_OF_FEED_ONE = "http://www.spiegel.de/index.rss"
IMG_URL_OF_FEED_ONE = "http://www.spiegel.de/spiegel.png"
LANG_OF_FEED_ONE = "de"
URL_OF_FEED_TWO = "http://www.lefigaro.fr/rss/figaro_international.xml"
IMG_URL_OF_FEED_TWO = "http://www.lefigaro.fr/favicon.png"
LANG_OF_FEED_TWO = "fr"


class RSSFeedRule(BaseRule):
    """

        Creates a RSSFeed object with random data and saves it to the database

    """

    def __init__(self):
        super().__init__()

        self.rss_feed = self._create_model_object()
        self.feed = self.rss_feed
        self.save(self.rss_feed)

        lang1 = Language.find_or_create(LANG_OF_FEED_ONE)
        url = Url.find_or_create(self.db.session, URL_OF_FEED_ONE)
        image_url = Url.find_or_create(self.db.session, IMG_URL_OF_FEED_ONE)
        self.feed1 = RSSFeed.find_or_create(self.db.session, url, "", "", image_url=image_url,
                                            language=lang1)
        self.save(self.feed1)

        lang2 = Language.find_or_create(LANG_OF_FEED_TWO)
        url2 = Url.find_or_create(self.db.session, URL_OF_FEED_TWO)
        image_url2 = Url.find_or_create(self.db.session, IMG_URL_OF_FEED_TWO)
        self.feed2 = RSSFeed.find_or_create(self.db.session,
                                            url2, "", "", image_url=image_url2, language=lang2)
        self.save(self.feed2)

    @staticmethod
    def _exists_in_db(obj):
        return RSSFeed.exists(obj)

    def _create_model_object(self):
        title = " ".join(self.faker.text().split()[:(randint(1, 10))])
        description = " ".join(self.faker.text().split()[:(randint(5, 20))])
        language = LanguageRule().random
        url = UrlRule().url
        image_url = UrlRule().url

        new_rss_feed = RSSFeed(url, title, description, image_url, language)

        if RSSFeed.exists(new_rss_feed):
            return self._create_model_object()

        return new_rss_feed
