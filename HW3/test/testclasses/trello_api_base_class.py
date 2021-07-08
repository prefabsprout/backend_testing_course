import requests


class TrelloAPIBaseClass:
    def __init__(self):
        self.base_url = "https://api.trello.com"
        self.parameters = dict()
        self.api_response = None

    def set_authentication_data(self, key, token):
        self.parameters["key"] = key
        self.parameters["token"] = token
        return self

    def get(self, api_route=""):
        self.api_response = requests.get(f"{self.base_url}{api_route}", params=self.parameters)
        self.parameters = dict()
        return self

    def post(self):
        self.api_response = requests.post(self.base_url, json=self.parameters)
        self.parameters = dict()
        return self

    def put(self):
        self.api_response = requests.put(self.base_url, json=self.parameters)
        self.parameters = dict()
        return self

    def delete(self, api_route=""):
        self.api_response = requests.delete(f"{self.base_url}{api_route}", params=self.parameters)
        self.parameters = dict()
        return self

    def should_status_code_be_as_expected(self, expected_status_code):
        assert self.api_response.status_code == expected_status_code, \
            f"Status code expected to be {expected_status_code}, not {self.api_response.status_code}"
        return self

    def should_text_response_be_as_expected(self, expected_response_text):
        assert self.api_response.text == expected_response_text, \
            f"Text response expected to be {expected_response_text}, not {self.api_response.text}"
        return self

    def should_json_attribute_contains_expected_values(self, json_attribute, expected_value):
        assert self.api_response.json()[json_attribute] == expected_value, \
            f"JSON attribute {json_attribute} contains {self.api_response.json()[json_attribute]} " \
            f"instead {expected_value}"
        return self

    def should_json_response_be_expected_length(self, expected_length):
        assert len(self.api_response.json()) == expected_length, f"JSON response length " \
                                                                 f"expected to be {expected_length}, " \
                                                                 f"not {len(self.api_response.json())}"
        return self
