import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from zeeguu_teacher_dashboard.util import classroom

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

    def test_format_class_table_data(self):
        duration = 14
        number_fake_students = 4
        fake_student = json.loads("""[{
                    "id": "0",
                    "name": "student0",
                    "email": "email_address",
                    "reading_time": 5000,
                    "exercises_done": 5000,
                    "last_article": "place holder article",
                    "reading_time_list": [
                        0,
                        0,
                        0,
                        2500,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        2500,
                        0,
                        0,
                        0,
                        0
                    ],
                    "exercise_time_list": [
                        0,
                        0,
                        0,
                        0,
                        2500,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        2500,
                        0
                    ]
                },
                {
                    "id": "1",
                    "name": "student1",
                    "email": "email_address",
                    "reading_time": 5000,
                    "exercises_done": 0,
                    "last_article": "place holder article",
                    "reading_time_list": [
                        0,
                        0,
                        0,
                        2500,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        2500,
                        0,
                        0,
                        0,
                        0
                    ],
                    "exercise_time_list": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                },
                {
                    "id": "2",
                    "name": "student2",
                    "email": "email_address",
                    "reading_time": 0,
                    "exercises_done": 5000,
                    "last_article": "place holder article",
                    "reading_time_list": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ],
                    "exercise_time_list": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        2500,
                        2500,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                },
                {
                    "id": "3",
                    "name": "student3",
                    "email": "email_address",
                    "reading_time": 0,
                    "exercises_done": 0,
                    "last_article": "place holder article",
                    "reading_time_list": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ],
                    "exercise_time_list": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                }]""")

        expected_student_return = []
        ideal_days = []
        now = datetime.today()

        for i in range(duration):
            ideal_days.append((now - timedelta(days=i)).strftime("%d-%m"))
        expected_student_return.append(ideal_days)

        for i in range(0, number_fake_students):
            day = []
            for j in range(0, duration):
                day.append({
                    "date": now.strftime("%d-%m"),
                    "reading": fake_student[i]['reading_time_list'][j],
                    "exercise": fake_student[i]['exercise_time_list'][j],
                    "reading_color": classroom._format_for_color(fake_student[i]['reading_time_list'][j]),
                    "exercise_color": classroom._format_for_color(fake_student[i]['exercise_time_list'][j])
                })
                now = now - timedelta(days=1);
            expected_student_return.append({'name': fake_student[i]['name'], 'day_list': day})

        assert classroom.format_class_table_data(fake_student, duration) == expected_student_return

    @patch('zeeguu_teacher_dashboard.util.classroom.api_post')
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

    @patch('zeeguu_teacher_dashboard.util.classroom.api_post')
    def test_remove_class(self, mock_api_post):
        class_id = 0
        classroom.remove_class(class_id)
        mock_api_post.assert_called_with('remove_cohort/' + str(class_id))

    @patch('zeeguu_teacher_dashboard.util.classroom.api_get')
    @patch('zeeguu_teacher_dashboard.util.classroom.json')
    def test_load_class_info(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        class_id = 0
        class_info = classroom.get_general_cohort_info(class_id)

        mock_api_get.assert_called_with("cohort_info/" + str(class_id))
        mock_json.loads.assert_called_with('text return value')
        assert class_info == 'json return value'

    @patch('zeeguu_teacher_dashboard.util.classroom.api_get')
    @patch('zeeguu_teacher_dashboard.util.classroom.json')
    def test_load_classes(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        classes = classroom.load_classes()

        mock_api_get.assert_called_with("cohorts_info")
        mock_json.loads.assert_called_with('text return value')
        assert classes == 'json return value'

    @patch('zeeguu_teacher_dashboard.util.classroom.api_get')
    @patch('zeeguu_teacher_dashboard.util.classroom.json')
    def test_load_students(self, mock_json, mock_api_get):
        mock = MagicMock()
        mock.text = 'text return value'

        mock_api_get.return_value = mock
        mock_json.loads.return_value = 'json return value'

        class_id = 0
        duration = 0
        students = classroom.load_students(class_id, duration)

        mock_api_get.assert_called_with("users_from_cohort/" + str(class_id) + '/' + str(duration))
        mock_json.loads.assert_called_with('text return value')
        assert students == 'json return value'

    @patch('zeeguu_teacher_dashboard.util.classroom.api_get')
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

    def test_format_for_color(self):
        assert classroom._format_for_color(0) == 0
        assert classroom._format_for_color(1) == 0
        assert classroom._format_for_color(2) == 1
        assert classroom._format_for_color(299) == 1
        assert classroom._format_for_color(300) == 2
        assert classroom._format_for_color(600) == 3
        assert classroom._format_for_color(900) == 4

    def test_add_student_learning_proportion(self):
        fake_students = json.loads("""[{
            "id": "0",
            "name": "student0",
            "email": "email_address",
            "reading_time": 5000,
            "exercises_done": 5000,
            "last_article": "place holder article",
            "reading_time_list": [
                0,
                0,
                0,
                2500,
                0,
                0,
                0,
                0,
                0,
                0,
                2500,
                0,
                0,
                0,
                0
            ],
            "exercise_time_list": [
                0,
                0,
                0,
                0,
                2500,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                2500,
                0
            ]
        },
        {
            "id": "1",
            "name": "student1",
            "email": "email_address",
            "reading_time": 5000,
            "exercises_done": 0,
            "last_article": "place holder article",
            "reading_time_list": [
                0,
                0,
                0,
                2500,
                0,
                0,
                0,
                0,
                0,
                0,
                2500,
                0,
                0,
                0,
                0
            ],
            "exercise_time_list": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]
        },
        {
            "id": "2",
            "name": "student2",
            "email": "email_address",
            "reading_time": 0,
            "exercises_done": 5000,
            "last_article": "place holder article",
            "reading_time_list": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "exercise_time_list": [
                0,
                0,
                0,
                0,
                0,
                0,
                2500,
                2500,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]
        },
        {
            "id": "3",
            "name": "student3",
            "email": "email_address",
            "reading_time": 0,
            "exercises_done": 0,
            "last_article": "place holder article",
            "reading_time_list": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "exercise_time_list": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ]
        }]""")

        appended_fake_students = classroom.add_student_learning_proportion(students=fake_students)
        assert (appended_fake_students[0]['learning_proportion']) == 50
        assert (appended_fake_students[1]['learning_proportion']) == 100
        assert (appended_fake_students[2]['learning_proportion']) == 0
        assert (appended_fake_students[3]['learning_proportion']) == 0

    @patch('zeeguu_teacher_dashboard.util.classroom.api_post')
    def test_edit_class_info(self, fake_api_post):
        class_id = 0
        name = 'name'
        invite_code = 0
        declared_level_min = 0
        declared_level_max = 10
        package = {'name': name, 'inv_code': invite_code, 'declared_level_min': declared_level_min,
                   'declared_level_max': declared_level_max}

        classroom.update_class_info(class_id, name, invite_code, declared_level_min, declared_level_max)
        fake_api_post.assert_called_with('update_cohort/' + str(class_id), package=package)


if __name__ == '__main__':
    unittest.main()
