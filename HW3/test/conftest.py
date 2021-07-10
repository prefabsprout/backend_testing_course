import pytest

from HW3.test.testclasses.trello_api_boards_сlass import TrelloAPIBoardsClass


def pytest_addoption(parser):
    parser.addoption("--key", action="store", default="")
    parser.addoption("--token", action="store", default="")


@pytest.fixture(scope="function")
def authentication_data(pytestconfig):
    return {"key": pytestconfig.getoption("key"), "token": pytestconfig.getoption("token")}


@pytest.fixture(scope="function")
def test_board_configuration(pytestconfig, authentication_data):
    trello_api_boards = TrelloAPIBoardsClass(authentication_data)
    trello_api_boards.board_name = "test_board"
    response = trello_api_boards.post()
    test_board_id = response.json()['id']
    yield test_board_id
    trello_api_boards.board_id = test_board_id
    trello_api_boards.delete()


@pytest.fixture(scope="function")
def board_with_lists_configuration(pytestconfig, authentication_data):
    trello_api_boards = TrelloAPIBoardsClass(authentication_data)
    trello_api_boards.board_name = "test_board_with_lists"
    trello_api_boards.default_lists_parameter = True
    response = trello_api_boards.post()
    board_with_lists_id = response.json()['id']
    yield board_with_lists_id
    trello_api_boards.board_id = board_with_lists_id
    trello_api_boards.delete()


#     trello_api_boards = TrelloAPIBoardsClass()
#     response = trello_api_boards \
#         .set_authentication_data(pytestconfig.getoption("key"), pytestconfig.getoption("token")) \
#         .set_board_name(name="test_board") \
#         .set_default_list_parameter(True) \
#         .post()
#     board_with_lists_id = response.json()['id']
#     yield board_with_lists_id
#     trello_api_boards \
#         .set_authentication_data(pytestconfig.getoption("key"), pytestconfig.getoption("token")) \
#         .set_board_id(board_with_lists_id) \
#         .delete()


@pytest.fixture(scope="function")
def trello_api_boards_instance(pytestconfig, authentication_data):
    return TrelloAPIBoardsClass(authentication_data)
