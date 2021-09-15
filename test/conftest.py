import json
from datetime import datetime

import pytest
import xmltodict
from bottle_postgresql import DictWrapper
from pytest_mock import mocker

from bgg_collection import create_user_collection, add_user_to_collection

@pytest.fixture
def request_user_not_found():
    with open('test/requests/user_not_found.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_user_with_0_buddies():
    with open('test/requests/user_with_0_buddies.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_user_with_3_buddies():
    with open('test/requests/user_with_3_buddies.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_user_with_30_buddies():
    with open('test/requests/user_with_30_buddies.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_wait_for_access():
    with open('test/requests/wait_for_access.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_invalid_username():
    with open('test/requests/invalid_username.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_rate_limit_exceeded():
    with open('test/requests/rate_limit_exceeded.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_0_games():
    with open('test/requests/collection_with_0_games.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_1_game():
    with open('test/requests/collection_with_1_game.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_multiple_versions():
    with open('test/requests/collection_with_multiple_versions.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_56_games():
    with open('test/requests/collection_with_56_games.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_ratings_asc():
    with open('test/requests/collection_with_ratings_asc.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_collection_with_ratings_random():
    with open('test/requests/collection_with_ratings_random.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def request_game_random():
    with open('test/requests/game_random.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def collection_foo_bar(mocker, request_collection_with_ratings_asc, request_collection_with_ratings_random):
    mocker.patch('database.select_games', return_value=[{'game_id': 0, 'dominant_colors': ['#e6d9d2', '#b43929']},
                                                        {'game_id': 1, 'dominant_colors': ['#e6d9d2', '#b43929']},
                                                        {'game_id': 2, 'dominant_colors': ['#cebfb7', '#351b1a']}])
    mocker.patch('database.insert_and_select_games', return_value=[{'game_id': 0, 'dominant_colors': ['#e6d9d2', '#b43929']},
                                                                   {'game_id': 1, 'dominant_colors': ['#e6d9d2', '#b43929']},
                                                                   {'game_id': 2, 'dominant_colors': ['#e6d9d2', '#b43929']},
                                                                   {'game_id': 3, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 4, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 5, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 6, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 7, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 8, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 9, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 10, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 11, 'dominant_colors': ['#cebfb7', '#351b1a']},
                                                                   {'game_id': 12, 'dominant_colors': ['#cebfb7', '#351b1a']}])
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_ratings_asc)
    mocker.patch('database.select_collection', return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_ratings_asc))}))
    collection, loading_status = create_user_collection("foo", [])
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_ratings_random)
    mocker.patch('database.select_collection', return_value=DictWrapper(
        {"username": "bar", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_ratings_random))}))
    collection, loading_status = add_user_to_collection(collection, loading_status, "bar")
    return collection, loading_status
