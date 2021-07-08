from HW3.test.testclasses.trello_api_boards_сlass import TrelloAPIBoardsClass


class TestTrelloAPIBoards:
    def test_board_creation_without_name(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_name(name=None) \
            .post() \
            .should_status_code_be_as_expected(400) \
            .should_text_response_be_as_expected("invalid value for name")

    def test_create_board_with_lists(self, authentication_data):
        # Create board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_name(name="test_board_with_default_lists_option") \
            .set_default_list_parameter(True) \
            .post() \
            .should_status_code_be_as_expected(200)
        # Get board ID
        board_with_lists_id = trello_api_boards.api_response.json()["id"]

        # Get board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(board_with_lists_id) \
            .get("/lists") \
            .should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("To Do") \
            .should_board_contains_list_with_name("Doing") \
            .should_board_contains_list_with_name("Done")

        # Delete board with lists
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(board_with_lists_id) \
            .delete() \
            .should_status_code_be_as_expected(200)

    def test_create_board_with_name_over_max_length(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_name(name="z" * 16385) \
            .post() \
            .should_status_code_be_as_expected(400)

    def test_update_board_name(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_board_name("sounds_like_a_better_test_name_thanks") \
            .put() \
            .should_json_attribute_contains_expected_values(json_attribute="name",
                                                            expected_value="sounds_like_a_better_test_name_thanks")

    def test_update_board_description(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_board_description("descriiiiiiiiiiiiiiiiiiiiiiption") \
            .put() \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values(json_attribute="desc",
                                                            expected_value="descriiiiiiiiiiiiiiiiiiiiiiption")

    def test_create_board_with_wrong_api_key(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data("0123456789", authentication_data["token"]) \
            .set_board_name(name="good_nice_board") \
            .post() \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid key")

    def test_create_board_with_wrong_token(self, authentication_data):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], "0123456789") \
            .set_board_name(name="good_nice_board") \
            .post() \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid token")

    def test_board_delete(self, authentication_data, test_board_configuration):
        # Delete board
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .delete() \
            .should_status_code_be_as_expected(200)

        # Check for deleted board existence
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get() \
            .should_status_code_be_as_expected(404)

    def test_get_single_board(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get() \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board")

    def test_board_can_be_closed(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .set_closed_status(True) \
            .put() \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board") \
            .should_json_attribute_contains_expected_values("closed", True)

    def test_get_memberships_list(self, authentication_data, test_board_configuration):
        trello_api_boards = TrelloAPIBoardsClass()
        trello_api_boards \
            .set_authentication_data(authentication_data["key"], authentication_data["token"]) \
            .set_board_id(test_board_configuration) \
            .get("/memberships") \
            .should_status_code_be_as_expected(200) \
            .should_json_response_be_expected_length(expected_length=1) \
            .should_board_contains_member_with_certain_type("admin")
