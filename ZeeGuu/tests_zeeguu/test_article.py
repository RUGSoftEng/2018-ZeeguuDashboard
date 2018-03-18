from unittest import TestCase

from tests_zeeguu.model_test_mixin import ModelTestMixIn

import zeeguu
from tests_zeeguu.rules.article_rule import ArticleRule
from tests_zeeguu.rules.language_rule import LanguageRule
from zeeguu.model import Topic, Article

session = zeeguu.db.session

SOME_ARTICLE_URL = 'http://www.lemonde.fr/idees/article/2018/02/21/formation-le-big-bang-attendra_5260297_3232.html'


class ArticleTest(ModelTestMixIn, TestCase):
    def setUp(self):
        super().setUp()
        self.article1 = ArticleRule().article
        self.article2 = ArticleRule().article
        self.language = LanguageRule.get_or_create_language("en")

    def test_articles_are_different(self):
        assert (self.article1.title != self.article2.title)

    def test_article_representation_does_not_error(self):
        assert self.article1.article_info()

    def test_add_topic(self):
        health = Topic("health", self.language)
        sports = Topic("sports", self.language)
        self.article1.add_topic(health)
        self.article1.add_topic(sports)
        assert len(self.article1.topics) == 2

    def test_find_or_create(self):
        self.new_art = Article.find_or_create(session, SOME_ARTICLE_URL)
        assert (self.new_art.fk_difficulty)

    def test_load_article_without_language_information(self):
        url = 'https://edition.cnn.com/2018/03/12/asia/kathmandu-plane-crash/index.html'
        art = Article.find_or_create(session, url)
        assert (art)
