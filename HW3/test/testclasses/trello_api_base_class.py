import requests


class TrelloAPIBaseClass:
    def __init__(self, authentication_data):
        self.base_url = "https://api.trello.com"
        self.parameters = {"key": authentication_data['key'],
                           "token": authentication_data['token']}

    @property
    def key(self):
        return self.parameters['key']

    @key.setter
    def key(self, key):
        self.parameters['key'] = key

    @property
    def token(self):
        return self.parameters['token']

    @token.setter
    def token(self, token):
        self.parameters['token'] = token

    def get(self, api_route=""):
        return requests.get(f"{self.base_url}{api_route}", params=self.parameters)

    def post(self):
        return requests.post(self.base_url, json=self.parameters)

    def put(self):
        return requests.put(self.base_url, json=self.parameters)

    def delete(self, api_route=""):
        return requests.delete(f"{self.base_url}{api_route}", params=self.parameters)
