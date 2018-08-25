import unittest
from unittest.mock import patch

from zeeguu_teacher_dashboard import app
from zeeguu_teacher_dashboard.forms.create_cohort import CreateCohort

"""
This file contains a test for the validate method of the form create_cohort.py. Testing is done via unittest and 
function patching via the mock module in the unittest package. See the documentation for unittest.mock. The tests in
this file use a white-box/black-box testing method.
"""


class TestCreateCohort(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('zeeguu_teacher_dashboard.forms.create_cohort.FlaskForm')
    @patch('zeeguu_teacher_dashboard.forms.create_cohort.verify_invite_code_exists')
    def test_validate(self, mock_verify, mock_form):
        app.config['SECRET_KEY'] = 'testing'

        with app.test_request_context() as context:
            cohort = CreateCohort()
            cohort.name.data = 'French'
            cohort.class_language_id.data = 'fr'
            cohort.max_students.data = 15
            cohort.inv_code.data = 'invitecode'
            cohort.submit.data = True

            mock_verify.return_value = False
            mock_form.validate.return_value = True
            assert cohort.validate()
