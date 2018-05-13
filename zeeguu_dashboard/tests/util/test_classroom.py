import unittest
from unittest.mock import patch, MagicMock

from app.util import classroom

"""
This file contains a test function for every function inside the utility classroom.py. Testing is done via unittest and 
function patching via the mock module in the unittest package. See the documentation for unittest.mock. The tests in
this file use a white-box testing method.
"""


class TestClassroom(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('app.util.classroom.api_post')
    def test_create_class(self, mock_api_post):
        name = 'class'
        inv_code = 'INV'
        max_students = 0
        language_id = 'fr'

        classroom.create_class(name, inv_code, max_students, language_id)
        mock_api_post.assert_called_with('create_own_cohort', {'name': name,
                                                               'inv_code': inv_code,
                                                               'max_students': max_students,
                                                               'language_id': language_id})

    @patch('app.util.classroom.api_post')
    def test_remove_class(self, mock_api_post):
        class_id = 0
        classroom.remove_class(class_id)
        mock_api_post.assert_called_with('remove_cohort/' + str(class_id))

    @patch('app.util.classroom.api_get')
    @patch('app.util.classroom.json')
    def test_load_class_info(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        class_id = 0
        class_info = classroom.load_class_info(class_id)

        mock_api_get.assert_called_with("cohort_info/" + str(class_id))
        mock_json.loads.assert_called_with('text return value')
        assert class_info == 'json return value'

    @patch('app.util.classroom.api_get')
    @patch('app.util.classroom.json')
    def test_load_classes(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        classes = classroom.load_classes()

        mock_api_get.assert_called_with("cohorts_info")
        mock_json.loads.assert_called_with('text return value')
        assert classes == 'json return value'

    @patch('app.util.classroom.api_get')
    @patch('app.util.classroom.json')
    def test_load_students(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        class_id = 0
        students = classroom.load_students(class_id)

        mock_api_get.assert_called_with("users_from_cohort/" + str(class_id))
        mock_json.loads.assert_called_with('text return value')
        assert students == 'json return value'

    @patch('app.util.classroom.api_get')
    def test_verify_invite_code_exists(self, mock_api_get):
        mock = MagicMock()
        mock.text = "OK"
        mock_api_get.return_value = mock

        inv_code = 0
        assert not classroom.verify_invite_code_exists(inv_code)
        mock_api_get.assert_called_with('invite_code_usable/' + str(inv_code))

        mock.text = 'NOPE'
        assert classroom.verify_invite_code_exists(inv_code)
        mock_api_get.assert_called_with('invite_code_usable/' + str(inv_code))


if __name__ == '__main__':
    unittest.main()
