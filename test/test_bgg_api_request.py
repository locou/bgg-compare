from bgg_request import handle_collection_request


def test_handle_request_smoke(mocker, request_wait_for_access):
    mocker.patch('bgg_request.request_collection', return_value=request_wait_for_access)
    assert handle_collection_request("foo")


def test_handle_request_username(mocker, request_wait_for_access):
    mocker.patch('bgg_request.request_collection', return_value=request_wait_for_access)
    assert handle_collection_request("foo")["username"] == "foo"


def test_handle_request_invalid_username(mocker, request_invalid_username):
    mocker.patch('bgg_request.request_collection', return_value=request_invalid_username)
    assert handle_collection_request("foo")["message"]["status"] == 0
    assert handle_collection_request("foo")["message"]["errors"] == "Invalid username specified"


def test_handle_request_rate_limit_exceeded(mocker, request_rate_limit_exceeded):
    mocker.patch('bgg_request.request_collection', return_value=request_rate_limit_exceeded)
    assert handle_collection_request("foo")["message"]["status"] == 0
    assert handle_collection_request("foo")["message"]["errors"] == "Rate limit exceeded."


def test_handle_request_with_no_games_status_1(mocker, request_collection_with_0_games):
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_0_games)
    assert handle_collection_request("foo")["message"]["status"] == 1


def test_handle_request_with_games_status_1(mocker, request_collection_with_1_game):
    mocker.patch('bgg_request.request_collection', return_value=request_collection_with_1_game)
    assert handle_collection_request("foo")["message"]["status"] == 1


def test_handle_request_wait_for_access(mocker, request_wait_for_access):
    mocker.patch('bgg_request.request_collection', return_value=request_wait_for_access)
    assert handle_collection_request("foo")["message"]["status"] == 0
    assert handle_collection_request("foo")["message"]["message"] == "Your request for this collection has been accepted and will be processed. Please try again later for access."

