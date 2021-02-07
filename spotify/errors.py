class SpotifyError(Exception):
    """Base exception class for spyotipy"""
    pass


class HTTPException(SpotifyError):
    """Exception thrown when a request to spotify api fails

    Attributes
    ----------
    response :class:`aiohttp.ClientResponse`
        The response of the failed Request

    status: :class:`int`
        The status code of the failed HTTP request.
    text: :class:`str`
        The text of the error.
    """
    def __init__(self, response, message):
        self.response = response
        self.status = response.status
        error = message.get("error")

        if isinstance(error, dict):
            self.text = error.get("message", "")
        else:
            self.text = message.get("error_description", "")

        fmt = "{0.status} {0.reason}"
        if self.text.strip():
            fmt += ": {1}"

        super().__init__(fmt.format(self.response, self.text))


class Forbidden(HTTPException):
    """Exception that's thrown when status code 403 occurs.
    Subclass of :exc:`HTTPException`
    """
    pass


class NotFound(HTTPException):
    """Exception that's thrown when status code 404 occurs.
    Subclass of :exc:`HTTPException`
    """
    pass


class ServerError(HTTPException):
    """Exception that's thrown when a 500 range status code occurs. (Spotify Server Problem)
    Subclass of :exc:`HTTPException`.
    """
    pass


class BearerError(HTTPException):
    pass
