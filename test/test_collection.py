import json
from datetime import datetime

import pytest
from pytest_lazyfixture import lazy_fixture
from bottle_postgresql import DictWrapper
from test.db_results.select_games_1_game import select_games_1_game
from test.db_results.select_games_56_games import select_games_56_games
from bgg_collection import create_user_collection, add_user_to_collection, calc_ratings, build_collection_url


@pytest.mark.parametrize(
    "parameter, expected",
    [
        (["own"], 21),
        (["prevowned"], 55),
        (["fortrade"], 54),
        (["want"], 55),
        (["wanttoplay"], 50),
        (["wanttobuy"], 48),
        (["wishlist1"], 54),
        (["wishlist2"], 55),
        (["wishlist3"], 47),
        (["wishlist4"], 55),
        (["wishlist5"], 55),
        (["preordered"], 54),
        (["notag"], 53),
        (["norating"], 15),
        (["nocomment"], 1),
        (["noplays"], 10),
        (["own", "prevowned"], 20),
        (["prevowned", "fortrade"], 53),
        (["fortrade", "want"], 53),
        (["want", "wanttoplay"], 49),
        (["wanttoplay", "wanttobuy"], 43),
        (["wanttobuy", "wishlist1"], 47),
        (["wishlist1", "wishlist2"], 53),
        (["wishlist2", "wishlist3"], 46),
        (["wishlist3", "wishlist4"], 46),
        (["wishlist4", "wishlist5"], 54),
        (["wishlist5", "preordered"], 53),
        (["preordered", "notag"], 51),
        (["notag", "norating"], 13),
        (["norating", "nocomment"], 1),
        (["nocomment", "noplays"], 0),
        (["noplays", "own"], 1),
    ]
)
def test_collection_hard_filter(parameter, expected, mocker, request_collection_with_56_games, select_games_56_games):
    mocker.patch("database.select_games", return_value=select_games_56_games)
    mocker.patch("database.select_collection", return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_56_games))}))
    collection, _ = create_user_collection("foo", parameter)
    assert len(collection) == expected


def test_create_user_collection_0_games(mocker, request_collection_with_0_games):
    mocker.patch("database.select_collection", return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_0_games))}))
    collection, _ = create_user_collection("foo", [])
    assert len(collection) == 0


def test_create_user_collection_1_game(mocker, request_collection_with_1_game, select_games_1_game):
    mocker.patch("database.select_games", return_value=select_games_1_game)
    mocker.patch("database.select_collection", return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_1_game))}))
    collection, _ = create_user_collection("foo", [])
    assert len(collection) == 1
    assert collection["307002"]["type"] == "boardgame"
    assert collection["307002"]["title"] == "Regicide"
    assert collection["307002"]["yearpublished"] == "2005"
    assert collection["307002"]["thumbnail"] is not None
    assert collection["307002"]["dominant_colors"] == ["#5b5255", "#9eb7b1"]
    assert collection["307002"]["stats"] == {"minplayers": 1, "maxplayers": 4, "minplaytime": 10, "maxplaytime": 30,
                                             "numowned": 656, "numcomments": 134, "numweights": 13,
                                             "averageweight": 2.08, "numrating": 415, "average": 7.7,
                                             "bayesaverage": 5.9}
    assert collection["307002"]["users"] == {
        "foo": {"rating": None, "diff_rating": None, "numplays": 0, "comment": "", "tags": {"notag": ("notag", None)},
                "lastmodified": "Aug 2021"}}
    assert collection["307002"]["user"] == {"rating": None, "numplays": 0, "comment": "", "tags": {"notag": ("notag", None)},
                                            "lastmodified": "2021-08-15 11:32:26"}


def test_create_user_collection_many_games(mocker, request_collection_with_56_games, select_games_56_games):
    mocker.patch("database.select_games", return_value=select_games_56_games)
    mocker.patch("database.select_collection", return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_56_games))}))
    collection, _ = create_user_collection("foo", [])
    assert len(collection) == 56
    assert collection["177210"]["type"] == "boardgame"
    assert collection["177210"]["title"] == "Eight Epics"
    assert collection["177210"]["yearpublished"] == "2015"
    assert collection["177210"]["thumbnail"] is not None
    assert collection["177210"]["dominant_colors"] == ['#534d4a', '#d9c7b1']
    assert collection["177210"]["stats"] == {'average': 5.9,
                                             'averageweight': 2.0,
                                             'bayesaverage': 5.6,
                                             'maxplayers': 8,
                                             'maxplaytime': 60,
                                             'minplayers': 1,
                                             'minplaytime': 15,
                                             'numcomments': 121,
                                             'numowned': 1075,
                                             'numrating': 427,
                                             'numweights': 16}
    assert collection["177210"]["users"] == {'foo': {'comment': '',
                                                     'diff_rating': None,
                                                     'lastmodified': 'Jan 2019',
                                                     'numplays': 0,
                                                     'rating': 6.0,
                                                     'tags': {'own': ('own', None)}}}
    assert collection["177210"]["user"] == {'comment': '',
                                            'lastmodified': '2019-01-16 01:05:50',
                                            'numplays': 0,
                                            'rating': 6.0,
                                            'tags': {'own': ('own', None)}}


def test_create_user_collection_rated_multiple_versions(mocker, request_collection_with_multiple_versions, select_games_1_game):
    mocker.patch("database.select_games", return_value=select_games_1_game)
    mocker.patch("database.select_collection", return_value=DictWrapper(
        {"username": "foo", "updated_at": datetime.now(),
         "collection": json.loads(json.dumps(request_collection_with_multiple_versions))}))
    collection, _ = create_user_collection("foo", [])
    assert len(collection) == 1


def test_add_user_to_collection_0_games():
    pass


def test_add_user_to_collection_1_game():
    pass


def test_add_user_to_collection_many_games():
    pass


def test_add_user_to_collection_rated_multiple_versions():
    pass


def test_add_user_to_collection_game_id_not_found():
    pass


def test_get_or_create_0_games():
    pass


def test_get_or_create_1_game():
    pass


def test_get_or_create_many_games():
    pass


def test_get_or_create_games_game_id_not_found():
    pass


def test_user_tags():
    pass


# @pytest.mark.parametrize(
#     "gameid, field, expected",
#     [
#         ("0", "mean_rating", 2),
#         ("0", "mean_diff_rating", None),
#         ("0", "median_rating", 2),
#         ("0", "sum_numplays", 11),
#         ("1", "sum_numplays", 201),
#         ("2", "mean_rating", 2),
#         ("2", "mean_diff_rating", None),
#         ("2", "median_rating", 2),
#         ("2", "sum_numplays", 5),
#         ("3", "mean_rating", 3.5),
#         ("3", "mean_diff_rating", 1),
#         ("3", "median_rating", 3.5),
#         ("5", "mean_rating", 5),
#         ("5", "mean_diff_rating", 0),
#         ("11", "mean_rating", None),
#         ("11", "mean_diff_rating", None),
#         ("11", "median_rating", None),
#     ],
# )
# def test_collection_calc_ratings(mocker, collection_foo_bar, gameid, field, expected):
#     mocker.patch("bgg_collection.get_or_create_games_color", return_value=dict())
#     collection, _ = collection_foo_bar
#     collection = calc_ratings(collection)
#     assert collection[gameid]["calc"][field] == expected


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
