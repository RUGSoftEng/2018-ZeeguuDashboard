import unittest
from unittest.mock import patch

from app.util import classroom


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('app.util.classroom.api_connection')
    def test_create_class(self, mock_api_connection):
        name = 'class'
        inv_code = 'INV'
        max_students = 0
        language_id = 'fr'

        classroom.create_class(name, inv_code, max_students, language_id)
        mock_api_connection.api_post.assert_called_with('create_own_cohort', {'name': name,
                                                                              'inv_code': inv_code,
                                                                              'max_students': max_students,
                                                                              'language_id': language_id})

    @patch('app.util.classroom.api_connection')
    def test_remove_class(self, mock_api_connection):
        dict = {}
        class_id = 0
        classroom.remove_class(class_id)
        mock_api_connection.api_post.assert_called_with('remove_cohort/' + str(class_id), dict)


if __name__ == '__main__':
    unittest.main()
