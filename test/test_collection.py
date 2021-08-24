import json
from datetime import datetime

import pytest
from pytest_lazyfixture import lazy_fixture
from bottle_postgresql import DictWrapper

from bgg_collection import create_user_collection


@pytest.mark.parametrize(
    "context, gameid, expected",
    [
        (lazy_fixture("fixture_request_with_1_game"), "20063", "Regicide"),
        (lazy_fixture("fixture_request_with_56_games"), "155122", "1066: Tears to Many Mothers"),
    ],
)
def test_handle_request_with_x_games(mocker, context, gameid, expected):
    mocker.patch('bgg_request.request_collection', return_value=context)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(context))}))
    collection, _ = create_user_collection("foo")
    assert collection[gameid]["display_name"] == expected


@pytest.mark.parametrize(
    "context, expected",
    [
        (lazy_fixture("fixture_request_with_0_games"), {}),
    ],
)
def test_handle_request_with_0_games(mocker, context, expected):
    mocker.patch('bgg_request.request_collection', return_value=context)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(context))}))
    collection, _ = create_user_collection("foo")
    assert collection == expected
