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
        duration = 0
        mock = MagicMock()
        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Chris'):
            mock.text = '["foo", {"bar":["baz", null, 1.0, 2]}]'
            mock_api_get.return_value = mock
            assert user.load_user_info(user_id, duration) == json.loads(mock.text)

    @patch('app.util.user.api_get')
    def test_load_user_data(self, mock_api_get):
        user655_json = """[{
                "date": "Sunday, 18 June 2017",
                "bookmarks":
                    [
                        {
                            "id": 18897,
                            "to": "With tense face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face tendu",
                            "context": "context0"
                        },
                        {
                            "id": 18897,
                            "to": "With tense face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face tendu",
                            "context": "context0"
                        },
                        {
                            "id": 18896,
                            "to": "To face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face",
                            "context": "context0"
                        },
                        {
                            "id": 18895,
                            "to": "at",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 15.08,
                            "learned_datetime": "",
                            "origin_rank": 12,
                            "starred": false,
                            "from": "à",
                            "context": "context0"
                        }
                 ]
            },
            {
                "date": "Monday, 19 June 2017",
                "bookmarks":
                    [
                        {
                            "id": 18879,
                            "to": "support",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "d’appui",
                            "context": "Elle est devenue le point d’appui dans la zone des forces spéciales américaines, et dans une moindre mesure britanniques, depuis que des révolutionnaires syriens sont parvenus, avec un tel appui occidental, à déloger Daech d’Al-Tanf en mars 2016."
                        },
                        {
                            "id": 18878,
                            "to": "lock",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "verrou",
                            "context": "Mais sa localisation stratégique sur la route entre Damas et Bagdad en fait le verrou du contrôle du triangle frontalier entre la Syrie, la Jordanie et l’Irak."
                        }
                    ]

            }]"""

        user655 = json.loads(user655_json)
        user655_filtered = user.filter_user_bookmarks(user655)
        user655_filtered_and_sorted = user.sort_user_bookmarks(user655_filtered)

        app = flask.Flask(__name__)

        with app.test_request_context('/?name=Chris'):
            mock = MagicMock()
            mock.text = user655_json
            mock_api_get.return_value = mock

            user_id = 0
            time = 0
            assert user.load_user_data(user_id, time, True) == user655_filtered_and_sorted

    def test_filter_user_bookmarks(self):
        day0 = {'bookmarks': [{'from': 'meer'}, {'from': 'zout'}, {'from': 'GRANATE'}]}
        day1 = {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}, {'from': 'alsjeblieft'}]}
        days = [day0, day1]
        expected_result = [day0, {'bookmarks': [{'from': 'hallo'}, {'from': 'alsjeblieft'}]}]

        real_result = user.filter_user_bookmarks(days)
        assert real_result == expected_result

    def test_get_correct_time(self):
        assert (user.get_correct_time('7')) == '1 week'
        assert (user.get_correct_time('14')) == '2 weeks'
        assert (user.get_correct_time('30')) == '1 month'
        assert (user.get_correct_time('180')) == '6 months'
        assert (user.get_correct_time('365')) == '1 year'

    def test_sort_user_bookmarks(self):
        base_case = []
        assert (user.sort_user_bookmarks([]) == base_case)
        fake_input = json.loads("""[{
                "date": "Sunday, 18 June 2017",
                "bookmarks":
                    [
                        {
                            "id": 18897,
                            "to": "With tense face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face tendu",
                            "context": "context0"
                        },
                        {
                            "id": 18897,
                            "to": "With tense face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face tendu",
                            "context": "context0"
                        },
                        {
                            "id": 18896,
                            "to": "To face",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "à face",
                            "context": "context0"
                        },
                        {
                            "id": 18895,
                            "to": "at",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 15.08,
                            "learned_datetime": "",
                            "origin_rank": 12,
                            "starred": false,
                            "from": "à",
                            "context": "context0"
                        }
                 ]
            },
            {
                "date": "Monday, 19 June 2017",
                "bookmarks":
                    [
                        {
                            "id": 18879,
                            "to": "support",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "d’appui",
                            "context": "context1"
                        },
                        {
                            "id": 18878,
                            "to": "lock",
                            "from_lang": "fr",
                            "to_lang": "en",
                            "title": "title0",
                            "url": "url0",
                            "origin_importance": 0,
                            "learned_datetime": "",
                            "origin_rank": "",
                            "starred": false,
                            "from": "verrou",
                            "context": "context2"
                        }
                    ]

            }]""")

        expected_output = [{
            'date': 'Sunday, 18 June 2017',
            'article_list':
                [
                    {
                        'title': 'title0',
                        'url': 'url0',
                        'sentence_list':
                            [
                                {
                                    'context': 'context0',
                                    'bookmarks':
                                        [
                                            {
                                                'id': 18897,
                                                'to': 'With tense face',
                                                'from_lang': 'fr',
                                                'to_lang': 'en',
                                                'title': 'title0',
                                                'url': 'url0',
                                                'origin_importance': 0,
                                                'learned_datetime': '',
                                                'origin_rank': '',
                                                'starred': False,
                                                'from': 'à face tendu',
                                                'context': 'context0'
                                            },
                                            {'id': 18897,
                                             'to': 'With tense face',
                                             'from_lang': 'fr',
                                             'to_lang': 'en',
                                             'title': 'title0',
                                             'url': 'url0',
                                             'origin_importance': 0,
                                             'learned_datetime': '',
                                             'origin_rank': '',
                                             'starred': False,
                                             'from': 'à face tendu',
                                             'context': 'context0'
                                             },
                                            {'id': 18896,
                                             'to': 'To face',
                                             'from_lang': 'fr',
                                             'to_lang': 'en',
                                             'title': 'title0',
                                             'url': 'url0',
                                             'origin_importance': 0,
                                             'learned_datetime': '',
                                             'origin_rank': '',
                                             'starred': False,
                                             'from': 'à face',
                                             'context': 'context0'
                                             },
                                            {'id': 18895,
                                             'to': 'at',
                                             'from_lang': 'fr',
                                             'to_lang': 'en',
                                             'title': 'title0',
                                             'url': 'url0',
                                             'origin_importance': 15.08,
                                             'learned_datetime': '',
                                             'origin_rank': 12,
                                             'starred': False,
                                             'from': 'à',
                                             'context': 'context0'
                                             }
                                        ]
                                }
                            ]
                    }
                ]},
            {'date': 'Monday, 19 June 2017', 'article_list': [{'title': 'title0', 'url': 'url0', 'sentence_list': [{
                'context': 'context1',
                'bookmarks': [
                    {
                        'id': 18879,
                        'to': 'support',
                        'from_lang': 'fr',
                        'to_lang': 'en',
                        'title': 'title0',
                        'url': 'url0',
                        'origin_importance': 0,
                        'learned_datetime': '',
                        'origin_rank': '',
                        'starred': False,
                        'from': 'd’appui',
                        'context': 'context1'}]},
                {
                    'context': 'context2',
                    'bookmarks': [
                        {
                            'id': 18878,
                            'to': 'lock',
                            'from_lang': 'fr',
                            'to_lang': 'en',
                            'title': 'title0',
                            'url': 'url0',
                            'origin_importance': 0,
                            'learned_datetime': '',
                            'origin_rank': '',
                            'starred': False,
                            'from': 'verrou',
                            'context': 'context2'}]}]}]}
        ]

        assert (user.sort_user_bookmarks(fake_input) == expected_output)
