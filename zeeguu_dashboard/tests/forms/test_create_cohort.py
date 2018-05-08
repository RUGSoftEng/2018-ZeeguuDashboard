import unittest
from unittest.mock import patch, MagicMock
from app.forms.create_cohort import CreateCohort
from app import app

class TestCreateCohort(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('app.forms.create_cohort.FlaskForm')
    @patch('app.forms.create_cohort.verify_invite_code_exists')
    def test_validate(self,mock_verify,mock_form):
        app.config['SECRET_KEY'] = 'testing'

        with app.test_request_context() as context:

            cohort = CreateCohort()
            cohort.class_name.data = 'French'
            cohort.class_language_id.data = 'fr'
            cohort.max_students.data = 15
            cohort.inv_code.data = 'invitecode'
            cohort.submit.data = True

            mock_verify.return_value = False
            mock_form.validate.return_value = True
            assert cohort.validate()