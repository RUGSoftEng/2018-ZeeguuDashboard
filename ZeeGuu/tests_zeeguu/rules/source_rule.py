import random

from sqlalchemy.orm.exc import NoResultFound

import zeeguu
from tests_zeeguu.rules.base_rule import BaseRule
from zeeguu.model.exercise_source import ExerciseSource


class SourceRule(BaseRule):
    """A Testing Rule class for ExerciseSources

    Has all supported sources as properties. Sources are created and
    saved to the database if they don't yet exist in the database.
    """

    sources = [
        "Recognize",
        "Translate",
        "ZeeKoe"
    ]

    @classmethod
    def __get_or_create_source(cls, source):
        try:
            return ExerciseSource.find(source)
        except NoResultFound:
            return cls.__create_new_source(source)

    @classmethod
    def __create_new_source(cls, source):
        index = cls.sources.index(source)
        source = cls.sources[index]

        if source is None:
            zeeguu.log("ExerciseSource {0} is not defined in SourceRule".format(source))
            raise KeyError

        new_source = ExerciseSource(source)

        cls.save(new_source)

        return new_source

    @property
    def recognize(self):
        return self.__get_or_create_source("Recognize")

    @property
    def translate(self):
        return self.__get_or_create_source("Translate")

    @property
    def zeekoe(self):
        return self.__get_or_create_source("ZeeKoe")

    @property
    def random(self):
        random_source = random.choice(self.sources)
        return self.__get_or_create_source(random_source)
