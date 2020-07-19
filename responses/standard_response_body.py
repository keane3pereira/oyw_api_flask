import json


class StandardResponseBody:

    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.__dict__ = { 'status': status, 'message': message }

    def json(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__