from .trello_api_base_class import TrelloAPIBaseClass


class TrelloAPIBoardsClass(TrelloAPIBaseClass):
    def __init__(self):
        super().__init__()
        self.base_url = f"{self.base_url}/1/boards"
        self.url_with_board_id = None
        self.test_board_id = None

    def set_board_name(self, name):
        self.parameters["name"] = name
        return self

    def set_board_description(self, description):
        self.parameters["desc"] = description
        return self

    def set_default_list_parameter(self, default_list_parameter):
        self.parameters["defaultLists"] = default_list_parameter
        return self

    def set_board_id(self, board_id):
        self.base_url = f"{self.base_url}/{board_id}"
        return self

    def set_closed_status(self, closed):
        self.parameters["closed"] = closed
        return self

    def should_board_contains_list_with_name(self, expected_name):
        result = filter(lambda board: board["name"] == expected_name, self.api_response.json())
        if not list(result):
            raise AssertionError(f"There is no board with name {expected_name}")
        return self

    def should_board_contains_member_with_certain_type(self, expected_member_type):
        result = filter(lambda board: board["memberType"] == expected_member_type, self.api_response.json())
        if not list(result):
            raise AssertionError(f"There is no member with type {expected_member_type}")
        return self

    def get_test_board_id(self):
        self.test_board_id = self.api_response.json()['id']
        return self
