import unittest
from unittest.mock import patch, MagicMock

from zeeguu_teacher_dashboard.util import permissions

"""
This file contains a test function for every function inside the utility permissions.py. Testing is done via unittest and 
function patching via the mock module in the unittest package. See the documentation for unittest.mock. The tests in
this file use a white-box/black-box testing method.
"""


class TestPermissions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('zeeguu_teacher_dashboard.util.permissions.session')
    @patch('zeeguu_teacher_dashboard.util.permissions.api_get')
    def test_check_session(self, mock_api_get, mock_sesison):
        mock_object = MagicMock()
        mock_object.text = 'OK'
        mock_api_get.return_value = mock_object

        assert permissions.check_session()

        mock_object.text = 'NOT OK'
        assert not permissions.check_session()

    @patch('zeeguu_teacher_dashboard.util.permissions.check_session')
    def test_has_session(func, mock_check_session):
        mock_check_session.return_value = True

        @permissions.has_session
        def test_function():
            return True

        assert test_function()
        mock_check_session.return_value = False
        assert test_function().status_code == 302

    @patch('zeeguu_teacher_dashboard.util.permissions.check_session')
    @patch('zeeguu_teacher_dashboard.util.permissions.api_get')
    def test_has_class_permission(self, mock_api_get, mock_check_session):
        @permissions.has_class_permission
        def test_function(class_id):
            return True

        mock = MagicMock()
        mock.text = "OK"
        mock_api_get.return_value = mock

        class_id = 1

        mock_check_session.return_value = True

        assert test_function(class_id=class_id)

        mock_check_session.return_value = False
        assert test_function(class_id=class_id).status_code == 302

        mock.text = "NOT OK"
        mock_api_get.return_value = mock

        mock_check_session.return_value = True
        assert test_function(class_id=class_id).status_code == 302

        mock_check_session.return_value = False
        assert test_function(class_id=class_id).status_code == 302

        mock_api_get.assert_called_with('has_permission_for_cohort/' + str(class_id))

    @patch('zeeguu_teacher_dashboard.util.permissions.app')
    @patch('zeeguu_teacher_dashboard.util.permissions.check_session')
    @patch('zeeguu_teacher_dashboard.util.permissions.api_get')
    def test_has_student_permission(self, mock_api_get, mock_check_session, mock_app):
        @permissions.has_student_permission
        def test_function(student_id, time):
            return True

        mock = MagicMock()
        mock.text = "OK"
        mock_api_get.return_value = mock

        config_mock = MagicMock()
        config_mock.config["DEFAULT_STUDENT_TIME"] = 14
        mock_app = config_mock

        student_id = 1

        mock_check_session.return_value = True

        assert test_function(student_id=student_id, time=14)
        assert test_function(student_id=student_id, time=600).status_code == 302

        mock_check_session.return_value = False
        assert test_function(student_id=student_id, time=14).status_code == 302
        assert test_function(student_id=student_id, time=600).status_code == 302

        mock.text = "NOT OK"
        mock_api_get.return_value = mock

        mock_check_session.return_value = True
        assert test_function(student_id=student_id, time=14).status_code == 302
        assert test_function(student_id=student_id, time=600).status_code == 302

        mock_check_session.return_value = False
        assert test_function(student_id=student_id, time=14).status_code == 302
        assert test_function(student_id=student_id, time=600).status_code == 302

        mock_api_get.assert_called_with('has_permission_for_user_info/' + str(student_id))
