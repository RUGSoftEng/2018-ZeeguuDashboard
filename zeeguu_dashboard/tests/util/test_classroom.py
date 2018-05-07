import unittest
from unittest.mock import patch

from app.util import classroom


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
        # TODO(christian): test the api_get().text return
        class_id = 0
        mock_json.loads.return_value = 'json return value'
        class_info = classroom.load_class_info(class_id)
        assert class_info == 'json return value'

    @patch('app.util.classroom.api_get')
    @patch('app.util.classroom.json')
    def test_load_classes(self, mock_json, mock_api_get):
        # TODO(christian): test the api_get().text return
        mock_json.loads.return_value = 'json return value'
        classes = classroom.load_classes()
        assert classes == 'json return value'

    @patch('app.util.classroom.api_get')
    @patch('app.util.classroom.json')
    def test_load_students(self, mock_json, mock_api_get):
        # TODO(christian): test the api_get().text return
        class_id = 0
        mock_json.loads.return_value = 'json return value'
        students = classroom.load_class_info(class_id)
        assert students == 'json return value'

    @patch('app.util.classroom.api_get')
    def test_verify_invite_code_exists(self, mock_api_get):
        # TODO(christian): test the api_get().text return
        classroom.verify_invite_code_exists(0)


if __name__ == '__main__':
    unittest.main()
