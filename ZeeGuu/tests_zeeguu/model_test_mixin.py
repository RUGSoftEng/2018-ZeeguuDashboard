import zeeguu.model

from faker import Faker

from unittest import TestCase


class ModelTestMixIn(TestCase):
    db = zeeguu.db

    def setUp(self):
        self.faker = Faker()
        self.db.create_all()

    def tearDown(self):
        super(ModelTestMixIn, self).tearDown()
        self.faker = None

        # sometimes the tearDown freezes on drop_all
        # and it seems that it's because there's still
        # a session open somewhere. Better call first:
        self.db.session.close()

        self.db.drop_all()
