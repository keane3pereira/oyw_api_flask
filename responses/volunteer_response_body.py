from responses.standard_response_body import StandardResponseBody
import flask


class GetAllVolunteersResponseBody(StandardResponseBody):

    def __init__(self, status, message, volunteers):
        StandardResponseBody.__init__(self, status, message)
        self.volunteers = volunteers
        self.__dict__ = { 'status': status, 'message': message, 'volunteers': volunteers }