import json
from datetime import datetime

import pytest
from pytest_lazyfixture import lazy_fixture
from bottle_postgresql import DictWrapper

from bgg_collection import create_user_collection, add_user_to_collection, calc_ratings, build_collection_url


# TODO: construct xml collection with each possible rating configuration
# TODO: test rating calc

@pytest.mark.parametrize(
    "context, gameid, expected",
    [
        (lazy_fixture("request_collection_with_1_game"), "20063", "Regicide"),
        (lazy_fixture("request_collection_with_56_games"), "155122", "1066: Tears to Many Mothers"),
    ],
)
def test_create_request_collection_with_games(mocker, context, gameid, expected):
    mocker.patch('bgg_request.request_collection', return_value=context)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(context))}))
    collection, _ = create_user_collection("foo")
    assert collection[gameid]["display_name"] == expected


def test_create_collection_0_games(mocker, request_collection_with_0_games):
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_0_games)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(request_collection_with_0_games))}))
    collection, _ = create_user_collection("foo")
    assert collection == {}


def test_add_collection(collection_foo_bar):
    _, loading_status = collection_foo_bar
    assert len(loading_status) == 2


@pytest.mark.parametrize(
    "gameid, field, expected",
    [
        ("0", "mean_rating", 2),
        ("0", "mean_diff_rating", None),
        ("0", "median_rating", 2),
        ("0", "sum_numplays", 11),
        ("1", "sum_numplays", 201),
        ("2", "mean_rating", 2),
        ("2", "mean_diff_rating", None),
        ("2", "median_rating", 2),
        ("2", "sum_numplays", 5),
        ("3", "mean_rating", 3.5),
        ("3", "mean_diff_rating", 1),
        ("3", "median_rating", 3.5),
        ("5", "mean_rating", 5),
        ("5", "mean_diff_rating", 0),
        ("11", "mean_rating", None),
        ("11", "mean_diff_rating", None),
        ("11", "median_rating", None),
    ],
)
def test_collection_calc_ratings(collection_foo_bar, gameid, field, expected):
    collection, _ = collection_foo_bar
    collection = calc_ratings(collection)
    assert collection[gameid]["calc"][field] == expected


def test_collection_build_url():
    loading_status = [
        {"username": "foo"},
        {"username": "bar"},
    ]
    loading_status = build_collection_url(loading_status)
    assert loading_status[0]["remove_collection_url"] == "bar"
    assert loading_status[1]["collection_url"] == "bar?add_user=foo"
    assert loading_status[1]["remove_collection_url"] == "foo"
