from unittest import TestCase

import zeeguu


class LanguageTest(TestCase):

    def test_languages_exists(self):
        zeeguu.log("tüst")
