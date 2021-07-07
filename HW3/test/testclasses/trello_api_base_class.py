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

    def get(self, api_route):
        result_request = requests.get(f"{self.base_url}{api_route}", params=self.parameters)
        self.parameters = dict()
        return result_request

    def post(self):
        self.api_response = requests.post(self.base_url, json=self.parameters)
        self.parameters = dict()
        return self

    def put(self):
        self.api_response = requests.put(self.base_url, json=self.parameters)
        self.parameters = dict()
        return self

    def delete(self, api_route):
        self.api_response = requests.delete(f"{self.base_url}{api_route}", params=self.parameters)
        self.parameters = dict()
        return self