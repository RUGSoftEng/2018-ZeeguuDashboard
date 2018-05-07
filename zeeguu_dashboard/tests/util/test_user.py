import json
import unittest
from unittest.mock import patch, MagicMock

import flask

from app.util import user


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
