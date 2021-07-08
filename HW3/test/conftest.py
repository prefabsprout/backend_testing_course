import pytest

from HW3.test.testclasses.trello_api_boards_сlass import TrelloAPIBoardsClass


def pytest_addoption(parser):
    parser.addoption("--key", action="store", default="")
    parser.addoption("--token", action="store", default="")


@pytest.fixture(scope="function")
def test_board_configuration(pytestconfig):
    trello_api_boards = TrelloAPIBoardsClass()
    trello_api_boards \
        .set_authentication_data(pytestconfig.getoption("key"), pytestconfig.getoption("token")) \
        .set_board_name(name="test_board") \
        .post() \
        .get_test_board_id()
    yield trello_api_boards.test_board_id
    trello_api_boards \
        .set_authentication_data(pytestconfig.getoption("key"), pytestconfig.getoption("token")) \
        .set_board_id(trello_api_boards.test_board_id) \
        .delete()


@pytest.fixture(scope="function")
def authentication_data(pytestconfig):
    return {"key": pytestconfig.getoption("key"), "token": pytestconfig.getoption("token")}
