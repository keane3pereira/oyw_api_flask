from responses.standard_response_body import StandardResponseBody
import flask


class LoginResponseBody(StandardResponseBody):

    def __init__(self, status, message, user):
        StandardResponseBody.__init__(self, status, message)
        self.user = user
        self.__dict__ = { 'status': status, 'message': message, 'user': user }