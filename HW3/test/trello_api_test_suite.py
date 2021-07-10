from HW3.test.testclasses.trello_api_boards_сlass import TrelloAPIBoardsClass
from HW3.test.testutils.api_response_checker import APIResponseChecker


class TestTrelloAPIBoards:
    def test_board_creation_without_name(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_name(name=None) \
            .post()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(400) \
            .should_text_response_be_as_expected("invalid value for name")

    def test_to_do_list_exists_in_board_with_default_lists(self, authentication_data, board_with_lists_configuration):
        # Get board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(board_with_lists_configuration) \
            .get("/lists")

        APIResponseChecker(response).should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("To Do")

    def test_doing_list_exists_in_board_with_default_lists(self, authentication_data, board_with_lists_configuration):
        # Get board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(board_with_lists_configuration) \
            .get("/lists")

        APIResponseChecker(response).should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("Doing")

    def test_done_list_exists_in_board_with_default_lists(self, authentication_data, board_with_lists_configuration):
        # Get board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(board_with_lists_configuration) \
            .get("/lists")

        APIResponseChecker(response).should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("Done")

    def test_create_board_with_name_over_max_length(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_name(name="z" * 16385) \
            .post()

        APIResponseChecker(response).should_status_code_be_as_expected(400)

    def test_update_board_name(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_board_name("better_test_name") \
            .put()

        APIResponseChecker(response).should_json_attribute_contains_expected_values(json_attribute="name",
                                                                                    expected_value="better_test_name")

    def test_update_board_description(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_board_description("descriiiiiiiiiiiiiiiiiiiiiiption") \
            .put()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values(json_attribute="desc",
                                                            expected_value="descriiiiiiiiiiiiiiiiiiiiiiption")

    def test_create_board_with_wrong_api_key(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data("0123456789", authentication_data["token"]) \
            .set_board_name(name="good_nice_board") \
            .post()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid key")

    def test_create_board_with_wrong_token(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], "0123456789") \
            .set_board_name(name="good_nice_board") \
            .post()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid token")

    def test_board_delete(self, authentication_data, test_board_configuration):
        # Delete board
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .delete()

        APIResponseChecker(response).should_status_code_be_as_expected(200)

        # Check for deleted board existence
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get()

        APIResponseChecker(response).should_status_code_be_as_expected(404)

    def test_get_single_board(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board")

    def test_board_can_be_closed(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_closed_status(True) \
            .put()

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board") \
            .should_json_attribute_contains_expected_values("closed", True)

    def test_get_memberships_list(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        response = trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get("/memberships")

        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_response_be_expected_length(expected_length=1) \
            .should_board_contains_member_with_certain_type("admin")
