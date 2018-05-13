import json
import unittest
from unittest.mock import patch, MagicMock

import flask

from app.util import user

"""
This file contains a test function for every function inside the utility user.py. Testing is done via unittest and 
function patching via the mock module in the unittest package. See the documentation for unittest.mock. The tests in
this file use a white-box/black-box testing method.
"""


class TestUser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('app.util.user.api_get')
    def test_load_user_info(self, mock_api_get):
        user_id = 0
        mock = MagicMock()
        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Chris'):
            mock.text = '["foo", {"bar":["baz", null, 1.0, 2]}]'
            mock_api_get.return_value = mock
            assert user.load_user_info(user_id) == json.loads(mock.text)

    @patch('app.util.user.api_get')
    def test_load_user_data(self, mock_api_get):
        day0 = {'bookmarks': [{'from': 'meer'}, {'from': 'zout'}, {'from': 'GRANATE'}]}
        day1 = {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}, {'from': 'alsjeblieft'}]}
        days = [day0, day1]
        expected_result = [day0, {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}]}]
        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Chris'):
            mock = MagicMock()
            mock.text = json.dumps(days)
            mock_api_get.return_value = mock

            user_id = 0
            time = 0
            assert user.load_user_data(user_id, time) == expected_result

    def test_filter_user_bookmarks(self):
        day0 = {'bookmarks': [{'from': 'meer'}, {'from': 'zout'}, {'from': 'GRANATE'}]}
        day1 = {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}, {'from': 'alsjeblieft'}]}
        days = [day0, day1]
        expected_result = [day0, {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}]}]

        real_result = user.filter_user_bookmarks(days)
        assert real_result == expected_result
