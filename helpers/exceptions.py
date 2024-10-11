class ChannelException(Exception):
    pass
class BadRequest(ChannelException):
    pass


class InternalServerError(ChannelException):
    pass


class AuthenticationError(ChannelException):
    """Parent class for any error that stops us from accessing details on a
    channel that we thought we could access."""

    # Default to thinking we can recover from an error.
    recoverable = True

    code = "authentication_error"
    message = "Cannot access account."


class InvalidCredentials(ChannelException):
    pass


class PropertyNotFound(ChannelException):
    pass


class PostingRatesError(ChannelException):
    pass


class ReservationNotFound(ChannelException):
    pass

class StatusCodeException(ChannelException):
    def __init__(self, message=None, status_code=None, response=None):
        # Invoke the parent constructor of Exception so that the exception has a message
        super().__init__(message)

        self.status_code = status_code
        self.message = message
        self.response = response