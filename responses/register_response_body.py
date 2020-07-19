from responses.standard_response_body import StandardResponseBody
import flask


class RegisterResponseBody(StandardResponseBody):

    def __init__(self, status, message, is_new, last_three_registers):
        StandardResponseBody.__init__(self, status, message)
        self.is_new = is_new
        self.last_three_registers = last_three_registers
        self.__dict__ = { 'status': status,
                        'message': message,
                        'is_new': is_new,
                        'last_three_registers': last_three_registers }