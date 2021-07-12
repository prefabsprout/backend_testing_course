from HW3.test.testutils.api_response_checker import APIResponseChecker


class TestTrelloAPIBoards:
    def test_board_creation_without_name(self, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_name = None

        # Request sending and response check
        response = trello_api_boards_instance.post()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(400) \
            .should_text_response_be_as_expected("invalid value for name")

    def test_to_do_list_exists_in_board_with_default_lists(self, board_with_lists_configuration,
                                                           trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = board_with_lists_configuration

        # Request sending and response check
        response = trello_api_boards_instance.get("/lists")
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("To Do")

    def test_doing_list_exists_in_board_with_default_lists(self, board_with_lists_configuration,
                                                           trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = board_with_lists_configuration

        # Request sending and response check
        response = trello_api_boards_instance.get("/lists")
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("Doing")

    def test_done_list_exists_in_board_with_default_lists(self, board_with_lists_configuration,
                                                          trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = board_with_lists_configuration

        # Request sending and response check
        response = trello_api_boards_instance.get("/lists")
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_board_contains_list_with_name("Done")

    def test_create_board_with_name_over_max_length(self, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_name = "z" * 16385

        # Request sending and response check
        response = trello_api_boards_instance.post()
        APIResponseChecker(response).should_status_code_be_as_expected(400)

    def test_update_board_name(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration
        trello_api_boards_instance.board_name = "better_test_name"

        # Request sending and response check
        response = trello_api_boards_instance.put()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values(json_attribute="name",
                                                            expected_value="better_test_name")

    def test_update_board_description(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration
        trello_api_boards_instance.board_description = "descriiiiiiiiiiiiiiiiiiiiiiption"

        # Request sending and response check
        response = trello_api_boards_instance.put()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values(json_attribute="desc",
                                                            expected_value="descriiiiiiiiiiiiiiiiiiiiiiption")

    def test_create_board_with_wrong_api_key(self, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.key = "0123456789"
        trello_api_boards_instance.board_name = "good_nice_board"

        # Request sending and response check
        response = trello_api_boards_instance.post()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid key")

    def test_create_board_with_wrong_token(self, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.token = "0123456789"
        trello_api_boards_instance.board_name = "good_nice_board"

        # Request sending and response check
        response = trello_api_boards_instance.post()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(401) \
            .should_text_response_be_as_expected("invalid token")

    def test_board_delete(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration

        # Delete request sending and response check
        delete_response = trello_api_boards_instance.delete()
        APIResponseChecker(delete_response).should_status_code_be_as_expected(200)

        # Check for deleted board existence
        get_response = trello_api_boards_instance.get()
        APIResponseChecker(get_response).should_status_code_be_as_expected(404)

    def test_get_single_board(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration

        # Request sending and response check
        response = trello_api_boards_instance.get()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board")

    def test_board_can_be_closed(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration
        trello_api_boards_instance.closed_status = True

        # Request sending and response check
        response = trello_api_boards_instance.put()
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_attribute_contains_expected_values("name", "test_board") \
            .should_json_attribute_contains_expected_values("closed", True)

    def test_get_memberships_list(self, test_board_configuration, trello_api_boards_instance):
        # Setting up request parameters
        trello_api_boards_instance.board_id = test_board_configuration

        # Request sending and response check
        response = trello_api_boards_instance.get("/memberships")
        APIResponseChecker(response) \
            .should_status_code_be_as_expected(200) \
            .should_json_response_be_expected_length(expected_length=1) \
            .should_board_contains_member_with_certain_type("admin")
