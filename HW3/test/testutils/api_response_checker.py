class APIResponseChecker:
    def __init__(self, response):
        self.response = response

    def should_status_code_be_as_expected(self, expected_status_code):
        assert self.response.status_code == expected_status_code, \
            f"Status code expected to be {expected_status_code}, not {self.response.status_code}"
        return self

    def should_text_response_be_as_expected(self, expected_response_text):
        assert self.response.text == expected_response_text, \
            f"Text response expected to be {expected_response_text}, not {self.response.text}"
        return self

    def should_json_attribute_contains_expected_values(self, json_attribute, expected_value):
        assert self.response.json()[json_attribute] == expected_value, \
            f"JSON attribute {json_attribute} contains {self.response.json()[json_attribute]} " \
            f"instead {expected_value}"
        return self

    def should_json_response_be_expected_length(self, expected_length):
        assert len(self.response.json()) == expected_length, f"JSON response length " \
                                                                 f"expected to be {expected_length}, " \
                                                                 f"not {len(self.response.json())}"
        return self

    def should_board_contains_list_with_name(self, expected_name):
        result = filter(lambda board: board["name"] == expected_name, self.response.json())
        if not list(result):
            raise AssertionError(f"There is no board with name {expected_name}")
        return self

    def should_board_contains_member_with_certain_type(self, expected_member_type):
        result = filter(lambda board: board["memberType"] == expected_member_type, self.response.json())
        if not list(result):
            raise AssertionError(f"There is no member with type {expected_member_type}")
        return self
