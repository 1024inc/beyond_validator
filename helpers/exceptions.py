class BadRequest(Exception):
    pass


class InternalServerError(Exception):
    pass


class AuthenticationError(Exception):
    """Parent class for any error that stops us from accessing details on a
    channel that we thought we could access."""

    # Default to thinking we can recover from an error.
    recoverable = True

    code = "authentication_error"
    message = "Cannot access account."


class InvalidCredentials(Exception):
    pass


class PropertyNotFound(Exception):
    pass


class PostingRatesError(Exception):
    pass


class ReservationNotFound(Exception):
    pass

class StatusCodeException(Exception):
    pass