from responses.standard_response_body import StandardResponseBody
import flask


class DataRetrievalBody(StandardResponseBody):
    
    def __init__(self, status, message, info, data):
        StandardResponseBody.__init__(self, status, message)
        self.info = info
        self.data = data
        self.__dict__ = {
            'info': info,
            'data': data
        }