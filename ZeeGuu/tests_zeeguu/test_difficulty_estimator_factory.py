from unittest import TestCase

from tests_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.language.difficulty_estimator_factory import DifficultyEstimatorFactory
from zeeguu.language.strategies.default_difficulty_estimator import DefaultDifficultyEstimator
from zeeguu.language.strategies.flesch_kincaid_difficulty_estimator import \
    FleschKincaidDifficultyEstimator
from zeeguu.language.strategies.frequency_difficulty_estimator import FrequencyDifficultyEstimator


class DifficultyEstimatorFactoryTest(ModelTestMixIn, TestCase):

    def test_ignore_capitalization(self):
        estimator_name = "FKINDEX"
        returned_estimator = DifficultyEstimatorFactory.get_difficulty_estimator(estimator_name)
        self.assertEqual(returned_estimator, FleschKincaidDifficultyEstimator)

    def test_unknown_type_returns_default(self):
        unknown_type = "unknown_type"
        returned_estimator = DifficultyEstimatorFactory.get_difficulty_estimator(unknown_type)
        self.assertEqual(returned_estimator, DefaultDifficultyEstimator)

    def test_returns_frequency_count_estimator(self):
        estimator_name = "FrequencyDifficultyEstimator"
        returned_estimator = DifficultyEstimatorFactory.get_difficulty_estimator(estimator_name)
        self.assertEqual(returned_estimator, FrequencyDifficultyEstimator)

    def test_returns_flesch_kincaid_estimator(self):
        estimator_name = "FleschKincaidDifficultyEstimator"
        returned_estimator = DifficultyEstimatorFactory.get_difficulty_estimator(estimator_name)
        self.assertEqual(returned_estimator, FleschKincaidDifficultyEstimator)

    def test_custom_names_flesch_kincaid_estimator(self):
        custom_names = ["FKIndex", "fk", "flesch-kincaid"]
        for name in custom_names:
            returned_estimator = DifficultyEstimatorFactory.get_difficulty_estimator(name)
            self.assertEqual(returned_estimator, FleschKincaidDifficultyEstimator)
