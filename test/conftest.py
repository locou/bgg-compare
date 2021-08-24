import pytest
import xmltodict


@pytest.fixture
def fixture_wait_for_access():
    with open('test/requests/wait_for_access.xml', 'r') as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_invalid_username():
    with open('test/requests/invalid_username.xml', 'r') as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_request_with_0_games():
    with open('test/requests/collection_with_0_games.xml', 'r') as f:
        data = f.read()
    return xmltodict.parse(data)


@pytest.fixture
def fixture_request_with_1_game():
    with open('test/requests/collection_with_1_game.xml', 'r') as f:
        data = f.read()
    return xmltodict.parse(data)