from responses.standard_response_body import StandardResponseBody
import flask


class ScanResponseBody(StandardResponseBody):
    
    def __init__(self, status, message, data):
        StandardResponseBody.__init__(self, status, message)
        self.data = data
        self.__dict__ = { 'status': status, 'message': message, 'data': data }