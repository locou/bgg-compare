import datetime

import pytest

from bgg_collection import create_user_collection


def test_handle_request_with_no_games_status_1(mocker):
    mocker.patch('database.select_collection', return_value=False)
    # assert create_user_collection("foo") is True
