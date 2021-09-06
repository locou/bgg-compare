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
    mocker.patch('database.select_games', return_value=dict())
    mocker.patch('database.insert_and_select_games', return_value=dict())
    mocker.patch('bgg_collection.get_or_create_games', return_value=dict())
    mocker.patch('bgg_request.request_collection', return_value=context)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(context))}))
    collection, _ = create_user_collection("foo")
    assert collection[gameid]["title"] == expected


def test_create_collection_0_games(mocker, request_collection_with_0_games):
    mocker.patch('bgg_collection.get_or_create_games', return_value=dict())
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_0_games)
    mocker.patch('database.select_collection', return_value=DictWrapper({"username": "foo", "updated_at": datetime.now(), "collection": json.loads(json.dumps(request_collection_with_0_games))}))
    collection, _ = create_user_collection("foo")
    assert collection == {}


def test_add_collection(mocker, collection_foo_bar):
    mocker.patch('bgg_collection.get_or_create_games_color', return_value=dict())
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
def test_collection_calc_ratings(mocker, collection_foo_bar, gameid, field, expected):
    mocker.patch('bgg_collection.get_or_create_games_color', return_value=dict())
    collection, _ = collection_foo_bar
    collection = calc_ratings(collection)
    assert collection[gameid]["calc"][field] == expected


@pytest.mark.parametrize(
    "key, loading_status, field, expected",
    [
        (0, [{"username": "foo"}], "collection_url", None),
        (0, [{"username": "foo"}], "remove_collection_url", None),
        (0, [{"username": "foo"}, {"username": "bar"}], "collection_url", "foo?add_user=bar"),
        (0, [{"username": "foo"}, {"username": "bar"}], "remove_collection_url", "bar"),
        (1, [{"username": "foo"}, {"username": "bar"}], "collection_url", "bar?add_user=foo"),
        (1, [{"username": "foo"}, {"username": "bar"}], "remove_collection_url", "foo"),
        (0, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "collection_url", "foo?add_user=bar&add_user=baz"),
        (0, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "remove_collection_url", "bar?add_user=baz"),
        (1, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "collection_url", "bar?add_user=foo&add_user=baz"),
        (1, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "remove_collection_url", "foo?add_user=baz"),
        (2, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "collection_url", "baz?add_user=foo&add_user=bar"),
        (2, [{"username": "foo"}, {"username": "bar"}, {"username": "baz"}], "remove_collection_url", "foo?add_user=bar"),
    ]
)
def test_collection_build_url_foo_bar_baz(key, loading_status, field, expected):
    loading_status = build_collection_url(loading_status)
    assert loading_status[key][field] == expected


@pytest.mark.parametrize(
    "return_value, expected",
    [
        (
                [
                    {
                        'game_id': 0,
                        'title': "Good Game",
                        "thumbnail": "http//url.img",
                        "type": "boardgame",
                        "dominant_colors": ["#aaa", "#bbb"],
                        "json": "json_import_by_mock",
                        "stats": {
                            "minplayers": 1,
                            "maxplayers": 4,
                            "minplaytime": 60,
                            "maxplaytime": 90,
                            "numowned": 8133,
                            "numcomments": 1075,
                            "numweights": 184,
                            "averageweight": 2.9185,
                            "numrating": 5477,
                            "average": 7.64815,
                            "bayesaverage": 7.11535,
                        },
                        "created_at": "",
                        "updated_at": ""
                    }
                ],
                [
                    {
                        'game_id': 0,
                        'title': "Good Game",
                        "thumbnail": "http//url.img",
                        "type": "boardgame",
                        "dominant_colors": ["#aaa", "#bbb"],
                        "json": "JASON",
                        "stats": {
                            "minplayers": 1,
                            "maxplayers": 4,
                            "minplaytime": 60,
                            "maxplaytime": 90,
                            "numowned": 8133,
                            "numcomments": 1075,
                            "numweights": 184,
                            "averageweight": 2.9,
                            "numrating": 5477,
                            "average": 7.6,
                            "bayesaverage": 7.1,
                        },
                        "created_at": "",
                        "updated_at": ""
                    }
                ],
        ),
    ]
)
def test_collection_request_item_entries(mocker, return_value, expected, request_collection_with_ratings_asc, request_game_random):
    mocker.patch('database.select_games', return_value=return_value)
    mocker.patch('database.insert_and_select_games', return_value=return_value)
    return_value[0]["json"] = request_game_random
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_ratings_asc)
    mocker.patch('database.select_collection', return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_ratings_asc))}))
    collection, loading_status = create_user_collection("foo")
    assert collection["0"]["title"] == expected[0]["title"]
    assert collection["0"]["thumbnail"] == expected[0]["thumbnail"]
    assert collection["0"]["type"] == expected[0]["type"]
    assert collection["0"]["dominant_colors"] == expected[0]["dominant_colors"]
    assert collection["0"]["stats"]["minplayers"] == expected[0]["stats"]["minplayers"]
    assert collection["0"]["stats"]["maxplayers"] == expected[0]["stats"]["maxplayers"]
    assert collection["0"]["stats"]["numowned"] == expected[0]["stats"]["numowned"]
    assert collection["0"]["stats"]["numcomments"] == expected[0]["stats"]["numcomments"]
    assert collection["0"]["stats"]["numweights"] == expected[0]["stats"]["numweights"]
    assert collection["0"]["stats"]["averageweight"] == expected[0]["stats"]["averageweight"]
    assert collection["0"]["stats"]["numrating"] == expected[0]["stats"]["numrating"]
    assert collection["0"]["stats"]["average"] == expected[0]["stats"]["average"]
    assert collection["0"]["stats"]["bayesaverage"] == expected[0]["stats"]["bayesaverage"]


# https://api.geekdo.com/xmlapi2/thing?id=192458&stats=1
# table item
# columns: uuid,
#          item_id,
#          title,
#          thumbnail,
#          type,
#          dominant_colors,
#          json,
#          created_at,
#          updated_at

# https://api.geekdo.com/xmlapi2/collection?username=Locou
# table collection
# columns: uuid,
#          user_id,
#          username,
#          number_of_games[sum, own, prevowned, preordered, wishlist, notag],
#          number_of_ratings[sum, own, prevowned, preordered, wishlist, notag],
#          number_of_comments[sum, own, prevowned, preordered, wishlist, notag],
#          json,
#          created_at,
#          updated_at

# https://api.geekdo.com/xmlapi2/user?name=msaari&buddies=1&hot=1&top=1
