from unittest import TestCase

from tests_zeeguu.model_test_mixin import ModelTestMixIn
from tests_zeeguu.rules.language_rule import LanguageRule
from tests_zeeguu.rules.user_rule import UserRule
from zeeguu.language.difficulty_estimator_factory import DifficultyEstimatorFactory
from zeeguu.language.strategies.default_difficulty_estimator import DefaultDifficultyEstimator
from zeeguu.language.strategies.frequency_difficulty_estimator import FrequencyDifficultyEstimator

SIMPLE_TEXT = "Das ist "
COMPLEX_TEXT = "Alle hatten in sein Lachen eingestimmt, hauptsächlich aus Ehrerbietung " \
               "gegen das Familienoberhaupt"


class FrequencyDifficultyEstimatorTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super().setUp()
        self.lan = LanguageRule().de
        self.user = UserRule().user

    def test_compute_very_simple_text_difficulty(self):
        estimator = DifficultyEstimatorFactory.get_difficulty_estimator("frequency")
        d1 = estimator.estimate_difficulty(SIMPLE_TEXT, self.lan, self.user)

        assert d1['discrete'] == 'EASY'
        assert d1['normalized'] < 0.1

    #Todo: Use a really difficuly text
    def test_compute_complex_text_difficulty(self):
        d1 = FrequencyDifficultyEstimator.estimate_difficulty(COMPLEX_TEXT, self.lan, self.user)

        assert d1['discrete'] == 'EASY'
        assert d1['normalized'] >= 0.25