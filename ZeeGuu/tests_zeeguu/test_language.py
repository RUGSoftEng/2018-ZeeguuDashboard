from unittest import TestCase

from sqlalchemy.orm.exc import NoResultFound

from tests_zeeguu.model_test_mixin import ModelTestMixIn
from tests_zeeguu.rules.language_rule import LanguageRule
from tests_zeeguu.rules.user_rule import UserRule
from zeeguu.model.language import Language


class LanguageTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.user = UserRule().user

    def test_languages_exists(self):
        language_should_be = LanguageRule().random

        try:
            language_to_check = Language.find(language_should_be.code)
        except NoResultFound:
            assert False, "No Language found in database"

        assert language_should_be.code == language_to_check.code \
               and language_should_be.name == language_to_check.name

    def test_get_all_languages(self):
        languages = LanguageRule.languages

        for lan in languages:
            assert LanguageRule.get_or_create_language(lan)

    def test_user_set_language(self):
        language_should_be = LanguageRule().random

        self.user.set_learned_language(language_should_be.code)
        assert self.user.learned_language.id == language_should_be.id

    def test_native_language(self):
        language_should_be = LanguageRule().random

        self.user.set_native_language(language_should_be.code)
        assert self.user.native_language.id == language_should_be.id
