from .trello_api_base_class import TrelloAPIBaseClass


class TrelloAPIBoardsClass(TrelloAPIBaseClass):
    def __init__(self, authentication_data):
        super().__init__(authentication_data)
        self.base_url = f"{self.base_url}/1/boards"

    @property
    def board_name(self):
        return self.parameters['name']

    @board_name.setter
    def board_name(self, board_name):
        self.parameters["name"] = board_name

    @property
    def board_description(self):
        return self.parameters['desc']

    @board_description.setter
    def board_description(self, board_description):
        self.parameters["desc"] = board_description

    @property
    def default_lists_parameter(self):
        return self.parameters["defaultLists"]

    @default_lists_parameter.setter
    def default_lists_parameter(self, default_list_parameter):
        self.parameters["defaultLists"] = default_list_parameter

    @property
    def board_id(self):
        return self.base_url

    @board_id.setter
    def board_id(self, board_id):
        self.base_url = f"{self.base_url}/{board_id}"

    @property
    def closed_status(self):
        return self.parameters["closed"]

    @closed_status.setter
    def closed_status(self, closed_status):
        self.parameters["closed"] = closed_status
