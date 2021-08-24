import pytest
import xmltodict


@pytest.fixture
def fixture_wait_for_access():
    with open('test/requests/wait_for_access.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_invalid_username():
    with open('test/requests/invalid_username.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_request_with_0_games():
    with open('test/requests/collection_with_0_games.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_request_with_1_game():
    with open('test/requests/collection_with_1_game.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_request_with_56_games():
    with open('test/requests/collection_with_56_games.xml', 'r', encoding="utf8") as f:
        data = f.read()
    return xmltodict.parse(data)
