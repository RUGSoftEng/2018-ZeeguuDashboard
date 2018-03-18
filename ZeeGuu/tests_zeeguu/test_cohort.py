from unittest import TestCase

from tests_zeeguu.model_test_mixin import ModelTestMixIn

import zeeguu
from tests_zeeguu.rules.cohort_rule import CohortRule
from zeeguu.model.teacher import Teacher
from zeeguu.model.teacher_cohort_map import TeacherCohortMap

session = zeeguu.db.session


class CohortTest(ModelTestMixIn, TestCase):
    def setUp(self):
        super().setUp()
        self.cohort_rule = CohortRule()
        self.cohort = self.cohort_rule.cohort
        self.user_t = self.cohort_rule.teacher
        self.student1 = self.cohort_rule.student1

    def test_teacher_has_students(self):

        self.assertTrue(self.user_t in self.cohort.get_teachers())
        self.assertTrue(self.student1 in self.cohort.get_students())

    def test_is_teacher(self):
        self.assertTrue(Teacher.from_user(self.user_t))
        self.assertFalse(Teacher.from_user(self.student1))

    def test_all_cohorts(self):
        teacher = Teacher.from_user(self.user_t)
        cohorts = teacher.get_cohorts()

        for c in cohorts:
            students = c.get_students()
            for student in students:
                self.assertTrue(student in self.cohort.get_students())

    def test_request_join(self):
        self.cohort.cur_students = 0
        self.assertTrue(self.cohort.request_join())
        self.assertTrue(self.cohort.cur_students==1)
        self.cohort.cur_students =9
        self.assertTrue(self.cohort.request_join())
        self.assertFalse(self.cohort.request_join())

    def test_undo_join(self):
        self.cohort.cur_students = 0
        self.cohort.undo_join()
        self.assertTrue(self.cohort.cur_students==0)
        self.cohort.cur_students = 5
        self.cohort.undo_join()
        self.assertTrue(self.cohort.cur_students==4)