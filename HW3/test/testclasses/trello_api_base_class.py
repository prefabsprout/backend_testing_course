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
        return requests.get(f"{self.base_url}{api_route}", params=self.parameters)

    def post(self):
        return requests.post(self.base_url, json=self.parameters)

    def put(self):
        return requests.put(self.base_url, json=self.parameters)

    def delete(self, api_route=""):
        return requests.delete(f"{self.base_url}{api_route}", params=self.parameters)
