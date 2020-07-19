from responses.standard_response_body import StandardResponseBody
import flask


class DisplayResponseBody(StandardResponseBody):
    
    def __init__(self, status, message, codes):
        StandardResponseBody.__init__(self, status, message)
        self.codes = codes
        self.__dict__ = { 'status': status, 'message': message, 'codes': codes }